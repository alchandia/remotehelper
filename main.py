#!/usr/bin/python3

import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path

host_lists = []
current_host = ["", "", "", "", ""]
home_user = str(Path.home())
home_app = os.path.dirname(os.path.realpath(__file__))

def isNotBlank (myString):
    if myString and myString.strip():        
        return True #myString is not None AND myString is not empty or blank
    return False #myString is None OR myString is empty or blank

def generate_host_list():

  # clean up and parse .ssh/config
  parse_ssh_command = "cat " + home_user + "/.ssh/config | grep -v '^#' | awk 'NF' > " + home_user + "/.ssh/config-remotehelper"
  os.system(parse_ssh_command)

  with open(home_user + "/.ssh/config-remotehelper") as fp:
      for line in fp:
          if line.startswith("Host"):
            current_host = ["", "", "", "", ""]
            current_host[0] = line.rstrip().lstrip().split(" ")[1]
          if line.startswith("  HostName"):
            current_host[1] = line.rstrip().lstrip().split(" ")[1]
          if line.startswith("  Port"):
            current_host[2] = line.rstrip().lstrip().split(" ")[1]
          if line.startswith("  User"):
            current_host[3] = line.rstrip().lstrip().split(" ")[1]            
          if line.startswith("  IdentityFile"):
            current_host[4] = line.rstrip().lstrip().split(" ")[1].replace("~",home_user)

          # Add host to list only if they have all the data need it
          if isNotBlank(current_host[0]) and isNotBlank(current_host[1]) and isNotBlank(current_host[2]) and isNotBlank(current_host[3]) and isNotBlank(current_host[4]):
            # ignore duplicate host
            if (current_host[0],current_host[1],int(current_host[2]),current_host[3],current_host[4]) not in host_lists:
              host_lists.append((current_host[0],current_host[1],int(current_host[2]),current_host[3],current_host[4]))
            current_host = ["", "", "", "", ""]

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="RemoteHelper")
        self.set_border_width(10)
        self.set_icon_from_file(home_app + '/icon.png')

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        entrySearch = Gtk.Entry()
        entrySearch.set_placeholder_text("Type to filter by hostname...")
        entrySearch.connect("changed", self.on_entrySearch_changed)

        buttonSSH = Gtk.Button(label="SSH")
        buttonSSH.connect("clicked", self.on_buttonSSH_clicked)

        buttonSFTP = Gtk.Button(label="SFTP")
        buttonSFTP.connect("clicked", self.on_buttonSFTP_clicked)

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

        for i, column_title in enumerate(["Hostname", "IP", "Port", "UserName", "Key Path"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        select = self.treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

        self.grid.attach_next_to(entrySearch, self.scrollable_treelist, Gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(buttonSSH, entrySearch, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(buttonSFTP, buttonSSH, Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def host_filter_func(self, model, iter, data):
        if self.current_filter_host is None or self.current_filter_host == "None" or self.current_filter_host == "":
            return True
        else:
            value = model.get_value(iter, 0).lower()
            return True if self.current_filter_host in value else False
          
    def on_buttonSSH_clicked(self, widget):
      ssh_command = "/usr/bin/xfce4-terminal --tab -T " + current_host[3] + "@" + current_host[0] + " -e 'ssh -X -o StrictHostKeyChecking=no -p {} -i " + current_host[4] + " " + current_host[3] + "@" + current_host[1] + "' &"
      os.system(ssh_command.format(current_host[2]))

    def on_buttonSFTP_clicked(self, widget):
      if os.path.exists(home_user + "/.ssh/filezilla"):
        os.remove(home_user + "/.ssh/filezilla")
      os.symlink(current_host[4], home_user + "/.ssh/filezilla")
      sftp_command = "/usr/bin/filezilla sftp://" + current_host[3] + ":@" + current_host[1] + ":{} &"
      os.system(sftp_command.format(current_host[2]))

    def on_tree_selection_changed(self, selection):
      model, treeiter = selection.get_selected()
      if treeiter is not None:
          current_host[0] = model[treeiter][0]
          current_host[1] = model[treeiter][1]
          current_host[2] = model[treeiter][2]
          current_host[3] = model[treeiter][3]
          current_host[4] = model[treeiter][4]

    def on_entrySearch_changed(self, widget):
      self.current_filter_host = widget.get_text()
      self.host_filter.refilter()

generate_host_list()

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
