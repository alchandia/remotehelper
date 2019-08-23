import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path

def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False

host_lists = []
host = ""
hostname = ""
port = ""
key = ""
user = ""

# clean up .ssh/config
parse_ssh_command = "cat /home/i2b/.ssh/config | grep -v '^#' | awk 'NF' > /home/i2b/.ssh/config-python"
os.system(parse_ssh_command)

with open("/home/i2b/.ssh/config-python") as fp:
    for line in fp:
        if line.startswith("Host"):
          host = ""
          hostname = ""
          port = ""
          key = ""
          user = ""          
          host = line.rstrip().lstrip().split(" ")[1]
        if line.startswith("  HostName"):
          hostname = line.rstrip().lstrip().split(" ")[1]
        if line.startswith("  Port"):
          port = line.rstrip().lstrip().split(" ")[1]
        if line.startswith("  IdentityFile"):
          key = line.rstrip().lstrip().split(" ")[1].replace("~",str(Path.home()))
        if line.startswith("  User"):
          user = line.rstrip().lstrip().split(" ")[1]

        if isNotBlank(host) and isNotBlank(hostname) and isNotBlank(port) and isNotBlank(key) and isNotBlank(user):
          host_lists.append((host,hostname,int(port),user,key))
          host = ""
          hostname = ""
          port = ""
          key = ""
          user = ""

class MainWindow(Gtk.Window):

    selected_host = ["none", "none", "none", "none", "none"]

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

        select = self.treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        vbox.pack_start(self.treeview, True, True, 0)

        listbox.add(row)

        self.show_all()

    def host_filter_func(self, model, iter, data):
        if self.current_filter_host is None or self.current_filter_host == "None":
            return True
        else:
            return model[iter][0] == self.current_filter_host
          
    def on_buttonSSH_clicked(self, widget):
      ssh_command = "/usr/bin/gnome-terminal --tab -- ssh -p {} -i " + self.selected_host[4] + " " + self.selected_host[3] + "@" + self.selected_host[1]
      os.system(ssh_command.format(self.selected_host[2]))

    def on_buttonSFTP_clicked(self, widget):
      if os.path.exists("/home/i2b/.ssh/filezilla"):
        os.remove("/home/i2b/.ssh/filezilla")
      os.symlink(self.selected_host[4], "/home/i2b/.ssh/filezilla")
      sftp_command = "/usr/bin/filezilla sftp://" + self.selected_host[3] + ":" + self.selected_host[4] + "@" + self.selected_host[1] + ":{} &"
      os.system(sftp_command.format(self.selected_host[2]))

    def on_tree_selection_changed(self, selection):
      model, treeiter = selection.get_selected()
      if treeiter is not None:
          self.selected_host[0] = model[treeiter][0]
          self.selected_host[1] = model[treeiter][1]
          self.selected_host[2] = model[treeiter][2]
          self.selected_host[3] = model[treeiter][3]
          self.selected_host[4] = model[treeiter][4]
        
win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()