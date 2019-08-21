import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

host_lists = [("host1", "192.168.1.1", 22, "root", "~/.ssh/key1"),
                 ("host2", "192.168.1.2", 2222, "ec2-user", "~/.ssh/key2"),
                 ("host3", "192.168.1.3", 22, "manager", "~/.ssh/key3")]

class MainWindow(Gtk.Window):

    selected_host = "none"

    def __init__(self):
        Gtk.Window.__init__(self, title="RemoteHelper")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        # Header
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(vbox, True, True, 0)

        label = Gtk.Label("hostX")
        buttonSSH = Gtk.Button(label="SSH")
        buttonSSH.connect("clicked", self.on_buttonSSH_clicked)
        buttonSFTP = Gtk.Button(label="SFTP")
        buttonSFTP.connect("clicked", self.on_buttonSFTP_clicked)

        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(buttonSSH, True, True, 0)
        vbox.pack_start(buttonSFTP, True, True, 0)

        listbox.add(row)

        # TreeView
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(vbox, True, True, 0)

        #Creating the ListStore model
        self.host_listsstore = Gtk.ListStore(str, str, int, str, str)
        for host_ref in host_lists:
            self.host_listsstore.append(list(host_ref))
        self.current_filter_host = None

        #Creating the filter, feeding it with the liststore model
        self.host_filter = self.host_listsstore.filter_new()
        #setting the filter function, note that we're not using the
        self.host_filter.set_visible_func(self.host_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.host_filter)
        for i, column_title in enumerate(["Host", "IP", "Port", "UserName", "Key Path"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        scrollable_treelist.add(self.treeview)

        select = self.treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        vbox.pack_start(scrollable_treelist, True, True, 0)

        listbox.add(row)

        self.show_all()

    def host_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_host is None or self.current_filter_host == "None":
            return True
        else:
            return model[iter][0] == self.current_filter_host
          
    def on_buttonSSH_clicked(self, widget):
      os.system("/usr/bin/gnome-terminal -- ssh -p 22 -i ~/.ssh/key user@192.168.1.1")

    def on_buttonSFTP_clicked(self, widget):
      print(self.selected_host)

    # https://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html
    def on_tree_selection_changed(self, selection):
      model, treeiter = selection.get_selected()
      if treeiter is not None:
          print("You selected", model[treeiter][1])
          self.selected_host = model[treeiter][1]

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()