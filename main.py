import tkinter as tk
from tkinter import ttk
import os
from utils import Utils
from options import OptionsWindow
from paramiko import SSHConfig

basedir = os.path.dirname(__file__)

# Set icon on taskbar
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = "i2btech.remotehelper.0.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(tk.Tk):

    def populate_treeview(self):
        openssh_config = Utils.option_get("general", "path_openssh_config", main_window.label_messages)
        ssh_config = SSHConfig()
        user_config_file = os.path.expanduser(openssh_config)

        if not os.path.exists(user_config_file):
            self.update_label_messages("Error!!!: ssh config not found")
            return

        try:
            # Clean treeview
            self.tree.delete(*self.tree.get_children())

            with open(user_config_file) as f:
                ssh_config.parse(f)

            # Insert the data in Treeview widget    
            for host in ssh_config.get_hostnames():
                conf = ssh_config.lookup(host)

                # exclude all entries that do not have user and port, we assume they are not machines
                if conf.get('port') and conf.get('user'):
                    key_name = os.path.basename(conf.get('identityfile')[0]) + ".ppk"
                    key_location = os.path.dirname(openssh_config)
                    key_ppk_path = key_location + "/" + key_name
                    key_pem_path = conf.get('identityfile')[0]
                    self.tree.insert('', 'end', text="1", values=(host, conf.get('hostname'), conf.get('port'), conf.get('user'), key_ppk_path, key_pem_path))
            self.update_label_messages("")

        except Exception as e:
            self.update_label_messages("Error parsing the config file: " + openssh_config + ". Check the format")

    def open_terminal(self):
        curItem = self.tree.focus()
        if curItem:
            details = self.tree.item(curItem)
            hostname = details.get("values")[0]
            ip = details.get("values")[1]
            port = details.get("values")[2]
            user_name = details.get("values")[3]
            key = details.get("values")[5]

            Utils.open_terminal(self.update_label_messages, hostname, ip, port, user_name, key)
        else:
            self.update_label_messages("Error!!!: Please select a host")

    def open_winscp(self):
        curItem = self.tree.focus()
        if curItem: 
            details = self.tree.item(curItem)
            ip = details.get("values")[1]
            port = details.get("values")[2]
            user_name = details.get("values")[3]
            key = details.get("values")[4]

            Utils.open_winscp(self.update_label_messages, ip, port, user_name, key)
        else:
            self.update_label_messages("Error!!!: Please select a host")
        
    def open_window_options(self):
        OptionsWindow(self, self.populate_treeview)

    def update_label_messages(self, message):
        self.label_messages.config(text=message)
                                   
    def __init__(self):
        super().__init__()
        self.title('Remote Helper')

        # Add menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar)
        # add menu item
        self.file_menu.add_command(
            label='Options',
            command=self.open_window_options
        )
        self.file_menu.add_separator()
        # add menu item
        self.file_menu.add_command(
            label='Exit',
            command=self.destroy
        )
        # add the Options menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu
        )

        # Set the size of the tkinter window
        self.s = ttk.Style()

        # Layout
        # Create top and bottom frames
        self.top_frame = ttk.Frame(self, width=200,  height=400)
        self.top_frame.pack(side='top',  fill='both',  padx=10,  pady=5)
        self.top_bar = ttk.Frame(self.top_frame,  width=180,  height=185)
        self.top_bar.grid(row=2,  column=0,  padx=5,  pady=5)

        # Add a Treeview widget
        columns = ('hostname', 'ip', 'port', 'user_name', 'key_ppk', 'key_pem')
        columns_to_display = ('hostname', 'ip', 'port', 'user_name', 'key_ppk')
        self.tree = ttk.Treeview(self, column=columns, displaycolumns=columns_to_display, show='headings', height=5, selectmode=tk.BROWSE)
        self.tree.heading('hostname', text="Hostname")
        self.tree.column("hostname", minwidth=0, width=200, stretch=tk.NO)
        self.tree.heading('ip', text="IP")
        self.tree.column("ip", minwidth=0, width=100, stretch=tk.NO)
        self.tree.heading('port', text="Port")
        self.tree.column("port", minwidth=0, width=40, stretch=tk.NO)
        self.tree.heading('user_name', text="User Name")
        self.tree.column("user_name", minwidth=0, width=80, stretch=tk.NO)
        self.tree.heading('key_ppk', text="Private Key")
        self.tree.column("key_ppk", minwidth=0, width=500, stretch=tk.NO)
        self.tree.heading('key_pem', text="Private Key")
        self.tree.column("key_pem", minwidth=0, width=500, stretch=tk.NO)
        self.tree.pack()

        # Create a Label widget
        self.label_messages=ttk.Label(self, text="")
        self.label_messages.pack()

        ttk.Entry(self.top_bar).grid(row=1,  column=0,  padx=5,  pady=5)
        ttk.Button(self.top_bar,  text="SSH", width=25, command=self.open_terminal).grid(row=1,  column=1,  padx=5,  pady=5)
        ttk.Button(self.top_bar,  text="WinSCP", width=25, command=self.open_winscp).grid(row=1,  column=2,  padx=5,  pady=5)

        # Set icon on taskbar
        self.iconbitmap(os.path.join(basedir, "icon.ico"))

if __name__ == '__main__':
    main_window = MainWindow()

    # Populate treeview
    main_window.populate_treeview()

    main_window.mainloop()
