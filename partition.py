#!/usr/bin/env python

#Kickstart Configurator Authentication Options
#Copyright Red Hat, Inc. 2001
#Written by Brent Fox (bfox@redhat.com) and Tammy Fox (tfox@redhat.com)
#Created February, 2000 Brent Fox
#Last Modified: February 6, 2001 Brent Fox

from gtk import *
import GtkExtra

class partitionWindow(GtkWindow):
    def okClicked(self, args):        
#        print self.getData()
        self.destroy()

    def cancelClicked(self, args):
#        self.myNisClass.set_disabled()
#        self.myKerberosClass.set_disabled()
        self.destroy()

    def getData(self):
        buf = ""
	return buf


    def __init__(self, quit_cb=None):
        GtkWindow.__init__(self, WINDOW_TOPLEVEL)
        self.set_modal(TRUE)
        self.set_border_width(6)
        self.set_default_size(550, 100)		
        self.set_title("Disk Partitioning")

        self.vbox = GtkVBox()
        self.add(self.vbox)

        frame3 = GtkFrame("Disk Partitioning")
        self.vbox.pack_start(frame3)

        partVbox = GtkVBox()
        frame3.add(partVbox)

        mbrHbox = GtkHBox()
        partVbox.pack_start(mbrHbox)

        mbrLabel = GtkLabel("Clear Master Boot Record:")
        mbrHbox.pack_start(mbrLabel)

        mbrRadio1 = GtkRadioButton(None, "Yes")
        mbrHbox.pack_start(mbrRadio1)

        mbrRadio2 = GtkRadioButton(mbrRadio1, "No")
        mbrHbox.pack_start(mbrRadio2)

        clearHbox = GtkHBox()
        partVbox.pack_start(clearHbox)

        clearLabel = GtkLabel("Remove Existing Partitions:")
        clearHbox.pack_start(clearLabel)

        clearRadio1 = GtkRadioButton(None, "None")
        clearHbox.pack_start(clearRadio1)

        clearRadio2 = GtkRadioButton(clearRadio1, "All")
        clearHbox.pack_start(clearRadio2)

        clearRadio3 = GtkRadioButton(clearRadio1, "Linux")
        clearHbox.pack_start(clearRadio3)


        #---Partition table clist---#
        titles = ["Mount Point", "Type", "Size (M)", "Growable"]

        partClist = GtkCList(4, titles)
        partVbox.pack_start(partClist)

        partClist.set_column_width(0, 150)
        partClist.set_column_width(1, 150)
        partClist.set_column_width(2, 50)
        partClist.set_column_width(3, 20)

        s = [0]

##         def delPartition(_button, partClist=partClist, selected=s, myCount=myCount):
##             myCount.decrement()
##             partClist.remove(selected[0])
##             editButton.set_state(STATE_INSENSITIVE)
##             delButton.set_state(STATE_INSENSITIVE)
        
        def select_clist(_clist, r, c, event, selected=s):
            selected[0] = r
            editButton.set_sensitive(TRUE)
            delButton.set_sensitive(TRUE)

        def unselect_clist(_clist, r, c, event, selected=s):
            editButton.set_state(STATE_INSENSITIVE)
            delButton.set_state(STATE_INSENSITIVE)

##         def addPartition(args):
	
##             addWindow = GtkWindow()
##             addWindow.connect("delete_event", deleteEvent)
##             addWindow.set_title('Add Partition Entry')
##             addWindow.set_border_width(6)
##             addWindow.set_default_size(100, 50)

##             addTable = GtkTable(5, 2, FALSE)
##             addWindow.add(addTable)

##             addLabel1 = GtkLabel("Mount Point:")
##             addTable.attach(addLabel1, 0, 1, 0, 1)
	
##             mpCombo = GtkCombo()
##             addTable.attach(mpCombo, 1, 2, 0, 1)
##             list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
##             mpCombo.set_popdown_strings(list_items)
##             mpCombo.entry.set_editable(TRUE)

##             addLabel2 = GtkLabel("Filesystem Type:")
##             addTable.attach(addLabel2, 0, 1, 1, 2)
            
##             fsCombo = GtkCombo()
##             addTable.attach(fsCombo, 1, 2, 1, 2)
##             list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
##             fsCombo.set_popdown_strings(list_items)
##             fsCombo.entry.set_text("")
##             fsCombo.entry.set_editable(TRUE)
	
##             addLabel3 = GtkLabel("Size (M):")
##             addTable.attach(addLabel3, 0, 1, 2, 3)
            
##             sizeEntry = GtkEntry()
##             addTable.attach(sizeEntry, 1, 2, 2, 3)
            
##             addLabel4 = GtkLabel("Growable:")
##             addTable.attach(addLabel4, 0, 1, 3, 4)

##             growCombo = GtkCombo()
##             addTable.attach(growCombo, 1, 2, 3, 4)
##             list_items = [ "No", "Yes" ]			
##             growCombo.set_popdown_strings(list_items)
##             growCombo.list.select_item(0)
##             growCombo.entry.set_editable(FALSE)
	
##         def addEntry(args, addWindow=addWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, myCount=myCount):
##             a = mpCombo.entry.get_text()
##             b = fsCombo.entry.get_text()
##             c = sizeEntry.get_text()
##             d = growCombo.entry.get_text()

##             entry = [ a, b, c, d]
##             partClist.append(entry)
##             addWindow.destroy()
##             myCount.increment()

##             ok = GtkButton("OK")
##             addTable.attach(ok, 0, 1, 4, 5)
##             ok.connect("clicked", addEntry)

##             cancelAdd = GtkButton("Cancel")
##             addTable.attach(cancelAdd, 1, 2, 4, 5)
##             cancelAdd.connect("clicked", addWindow.hide)

##             addWindow.show_all()


##         def editPartition(args, partClist=partClist, selection=s):
	
##             editWindow = GtkWindow()
##             editWindow.connect("delete_event", deleteEvent)
##             editWindow.set_title('Edit Partition Entry')
##             editWindow.set_border_width(6)
##             editWindow.set_default_size(100, 50)

##             editTable = GtkTable(5, 2, FALSE)
##             editWindow.add(editTable)

##             editLabel1 = GtkLabel("Mount Point:")
##             editTable.attach(editLabel1, 0, 1, 0, 1)
	
##             mpCombo = GtkCombo()
##             editTable.attach(mpCombo, 1, 2, 0, 1)
##             list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
##             mpCombo.set_popdown_strings(list_items)
##             mpCombo.entry.set_text("")
##             mpCombo.entry.set_editable(TRUE)

##             editLabel2 = GtkLabel("Filesystem Type:")
##             editTable.attach(editLabel2, 0, 1, 1, 2)

##             fsCombo = GtkCombo()
##             editTable.attach(fsCombo, 1, 2, 1, 2)
##             list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
##             fsCombo.set_popdown_strings(list_items)
##             fsCombo.entry.set_text("")
##             fsCombo.entry.set_editable(FALSE)
	
##             editLabel3 = GtkLabel("Size (M):")
##             editTable.attach(editLabel3, 0, 1, 2, 3)

##             sizeEntry = GtkEntry()
##             editTable.attach(sizeEntry, 1, 2, 2, 3)

##             editLabel4 = GtkLabel("Growable:")
##             editTable.attach(editLabel4, 0, 1, 3, 4)

##             growCombo = GtkCombo()
##             editTable.attach(growCombo, 1, 2, 3, 4)
##             list_items = [ "No", "Yes" ]			
##             growCombo.set_popdown_strings(list_items)
##             growCombo.entry.set_editable(FALSE)

##             for i in range(4):
## 		if i == 0:
##                     mpCombo.entry.set_text(partClist.get_text(s[0], i))
## 		elif i == 1:
##                     fsCombo.entry.set_text(partClist.get_text(s[0], i))
## 		elif i == 2:
##                     sizeEntry.set_text(partClist.get_text(s[0], i))
## 		elif i == 3:
##                     growCombo.entry.set_text(partClist.get_text(s[0], i))
			

##             def editEntry(args, editWindow=editWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, selected=s):
## 		a = mpCombo.entry.get_text()
## 		b = fsCombo.entry.get_text()
## 		c = sizeEntry.get_text()
## 		d = growCombo.entry.get_text()

## 		partClist.remove(selected[0])

## 		entry = [ a, b, c, d]
## #		partClist.append(entry)
## 		partClist.insert(selected[0], entry)
## 		editWindow.destroy()
		
## 		editButton.set_state(STATE_INSENSITIVE)
## 		delButton.set_state(STATE_INSENSITIVE)



##             okEdit = GtkButton("OK")
##             editTable.attach(okEdit, 0, 1, 4, 5)
##             okEdit.connect("clicked", editEntry)

##             cancelEdit = GtkButton("Cancel")
##             editTable.attach(cancelEdit, 1, 2, 4, 5)
##             editWindow.show_all()

##             def exitEdit(cancelEdit=cancelEdit, editWindow=editWindow):
## 		editWindow.hide()

##             cancelEdit.connect("clicked", exitEdit)

##         def deleteEvent(win, event=None):
##             win.destroy()
##             return TRUE

        bootPartition = ["/boot", "ext2", "35", "No"]
        partClist.append(bootPartition)

        swapPartition = ["", "Linux Swap", "128", "No"]
        partClist.append(swapPartition)

        rootPartition = ["/", "ext2", "1000", "Yes"]
        partClist.append(rootPartition)

        partHbox = GtkHBox()
        partVbox.pack_start(partHbox)

        addButton = GtkButton("Add")
#        addButton.connect("clicked", addPartition)
        partHbox.pack_start(addButton)

        editButton = GtkButton("Edit")
#        editButton.connect("clicked", editPartition)
        partHbox.pack_start(editButton)
        editButton.set_state(STATE_INSENSITIVE)

        delButton = GtkButton("Delete")
#        delButton.connect("clicked", delPartition)
        partHbox.pack_start(delButton)
        delButton.set_state(STATE_INSENSITIVE)

        partClist.connect("select_row", select_clist)
        partClist.connect("unselect_row", unselect_clist)


        self.show_all()
