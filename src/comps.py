#!/usr/bin/python

class ComponentSet:
    def __len__(self):
	return len(self.comps)

    def __getitem__(self, key):
	if (type(key) == types.IntType):
	    return self.comps[key]
	return self.compsDict[key]

    def getSelectionState(self):
	compsState = []
	for comp in self.comps:
	    compsState.append((comp, comp.getState()))

	pkgsState = []
	for pkg in self.packages.list():
	    pkgsState.append((pkg, pkg.getState()))

	return (compsState, pkgsState)

    def setSelectionState(self, pickle):
	(compsState, pkgsState) = pickle

        for (comp, state) in compsState:
	    comp.setState(state)

	for (pkg, state) in pkgsState:
	    pkg.setState(state)
	    
    def sizeStr(self):
	megs = self.size()
	if (megs >= 1000):
	    big = megs / 1000
	    little = megs % 1000
	    return "%d,%03dM" % (big, little)

	return "%dM" % (megs)

    def totalSize(self):
	total = 0
	for pkg in self.packages.list():
	    total = total + (pkg[rpm.RPMTAG_SIZE] / 1024)
	return total

    def size(self):
	size = 0
	for pkg in self.packages.list():
	    if pkg.isSelected(): size = size + (pkg[rpm.RPMTAG_SIZE] / 1024)

	return size / 1024

    def keys(self):
	return self.compsDict.keys()

    def exprMatch(self, expr, tags = [ "lang", "arch" ]):
        theTags = []
        for tag in tags:
            theTags.append(tag)

        # no expression == true
        if not expr:
            return 1

        # XXX preserve backwards compatible behavior
        if self.allLangs and "lang" in theTags:
            theTags.remove ("lang")

        if "lang" in theTags:
            if os.environ.has_key('LINGUAS'):
                langs = split (os.environ['LINGUAS'], ':')
                if len (langs) == 1 and not langs[0]:
                    langs = None
            else:
                if os.environ.has_key('LANG'):
                    langs = [ os.environ['LANG'] ]
                else:
                    langs = None

            if langs == None:
                # no languages specified, install them all
                theTags.remove ("lang")

	if expr[0] != '(':
	    raise ValueError, "leading ( expected"
	expr = expr[1:]
	if expr[len(expr) - 1] != ')':
	    raise ValueError, "bad comps file [missing )]"
	expr = expr[:len(expr) - 1]

	exprList = split(expr, 'and')
	truth = 1
	for expr in exprList:
	    l = split(expr)

            if l[0] == "lang":
                if theTags and "lang" not in theTags:
                    newTruth = 1
                else:
		    #print "check", l, "in", langs
                    if len(l) != 2:
                        raise ValueError, "too many arguments for lang"
                    if l[1] and l[1][0] == "!":
                        newTruth = l[1][1:] not in langs
                    else:
                        newTruth = l[1] in langs
	    elif l[0] == "arch":
                if theTags and "arch" not in theTags:
                    newTruth = 1
                if len(l) != 2:
                    raise ValueError, "too many arguments for arch"
                if l[1] and l[1][0] == "!":
                    newTruth = l[1][1:] not in self.archList
                else:
                    newTruth = l[1] in self.archList
	    else:
		s = "unknown condition type %s" % (l[0],)
		raise ValueError, s

	    truth = truth and newTruth
	return truth

    def readCompsFile(self, filename, packages):
        connected = 0
        while not connected:
            try:
		file = urllib.urlopen(filename)
            except IOError, (errnum, msg):
		log("IOError %s occured getting %s: %s", filename,
			errnum, str(msg))
                time.sleep(5)
            else:
                connected = 1

	lines = file.readlines()

	file.close()
	top = lines[0]
	lines = lines[1:]
	if (top != "3\n" and top != "4\n"):
	    raise TypeError, "comp file version 3 or 4 expected"
	
	comp = None
        conditional = None
	self.comps = []
	self.compsDict = {}
        self.expressions = {}
	for l in lines:
	    l = strip (l)
	    if (not l): continue
            expression = None

	    if (find(l, ":") > -1):
		(expression, l) = split(l, ":", 1)
                expression = strip (expression)
                l = strip(l)
                if expression and not expression[0] == '(':
                    # normalize expressions to all be of () type
                    expression = "(arch %s)" % (expression,)
                if not self.exprMatch (expression, tags = [ "arch" ]):
                    continue

	    if (find(l, "?") > -1):
                (trash, cond) = split (l, '?', 1)
                (cond, trash) = split (cond, '{', 1)
                conditional = self.compsDict[strip (cond)]
                continue

	    if (comp == None):
		(default, l) = split(l, None, 1)
		hidden = 0
		if (l[0:6] == "--hide"):
		    hidden = 1
		    (foo, l) = split(l, None, 1)
                (l, trash) = split(l, '{', 1)
                l = strip (l)
                if l == "Base":
                    hidden = 1
		comp = Component(self, l, default == '1', hidden)
	    elif (l == "}"):
                if conditional:
                    conditional = None
                else:
                    self.comps.append(comp)
                    self.compsDict[comp.name] = comp
                    comp = None
	    else:
		if (l[0] == "@"):
		    (at, l) = split(l, None, 1)
		    comp.addInclude(self.compsDict[l])
		else:
                    if conditional:
			# Let both components involved in this conditional
			# know what's going on.
                        comp.addConditionalPackage (conditional, packages[l])
			conditional.addConditionalPackage (comp, packages[l])
                    elif expression:
                        # this is a package with some qualifier prefixing it
                        # XXX last expression noted wins when setting up Everything.
                        self.expressions[packages[l]] = expression
                        comp.addPackageWithExpression (expression, packages[l])
                    else:
                        # if this package is listed anywhere without an expression, it can go in Everything.
                        self.expressions[packages[l]] = None
                        # this is a package.
                        comp.addPackage(packages[l])

        everything = Component(self, N_("Everything"), 0, 0)
        for package in packages.keys ():
	    if not ExcludePackages.has_key(packages[package][rpm.RPMTAG_NAME]):
                if self.expressions.has_key (packages[package]):
                    everything.addPackageWithExpression (self.expressions[packages[package]],
                                                         packages[package])
                else:
                    everything.addPackage (packages[package])
        self.comps.append (everything)
        self.compsDict["Everything"] = everything

	for comp in self.comps:
	    comp.setDefaultSelection()

    def updateSelections(self):
	for comp in self.comps:
            if comp.isSelected ():
                for pkg in comp.pkgs:
                    pkg.updateSelectionCache()
        
    def __repr__(self):
	s = ""
	for n in self.comps:
	    s = s + "{ " + n.name + " [";
	    for include in n.includes:
		s = s + " @" + include.name

	    for package in n:
		s = s + " " + str(package)
	    s = s + " ] } "

	return s

    def __init__(self, file, hdlist, arch = None, matchAllLang = 0):
        self.allLangs = matchAllLang
        self.archList = []
	if not arch:
	    import iutil
	    arch = iutil.getArch()

        self.archList.append(arch)

# always set since with can have i386 arch with i686 arch2, for example
#	arch2 = None
#	if arch == "sparc" and os.uname ()[4] == "sparc64":
#	    arch2 = "sparc64"
#
        arch2 = os.uname ()[4]
        if not arch2 in self.archList:
            self.archList.append (arch2)
        
	self.packages = hdlist
	self.readCompsFile(file, self.packages)
