import gtk
import gobject

class ProgressWindow(gtk.Window):
    def __init__(self, top_level, title="system-config-kickstart", label=""):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_deletable(False)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_transient_for(top_level)
        self.set_modal(True)

        self.set_title(title)

        self.label = gtk.Label(label)
        self.label.show()

        vbox = gtk.VBox()
        vbox.set_spacing(10)
        vbox.set_border_width(10)
        vbox.show()

        self.timer = None

        vbox.pack_start(self.label)

        self.add(vbox)

    def set_label(self, label):
        self.label.set_text(label)

    def next_task(self, *args, **kwargs):
        while gtk.events_pending():
            gtk.main_iteration()

    def stop(self):
        if self.timer:
            gobject.source_remove(self.timer)
            self.timer = None

    def show(self):
        gtk.Window.show(self)

    def hide(self):
        gtk.Window.hide(self)

    start = end = progressbar = next_task

