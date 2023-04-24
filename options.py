import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from utils import Utils

class OptionsWindow(tk.Toplevel):     

    def search_openssh_config(self):
        selected_file = filedialog.askopenfilename()
        if not selected_file == "":
            self.strvar_openssh.set(selected_file)

    def search_winscp_exec(self):
        selected_file = filedialog.askopenfilename()
        if not selected_file == "":
            self.strvar_winscp.set(selected_file)

    def save_changes(self):
        Utils.option_set("general", "path_openssh_config", self.strvar_openssh.get())
        Utils.option_set("general", "path_winscp_exe", self.strvar_winscp.get())
        Utils.option_set("general", "wsl_distro", self.strvar_combo.get())
        self.m_populate_treeview()
        self.destroy()

    def __init__(self, master, populate_treeview):

        super().__init__(master)
        self.m_populate_treeview = populate_treeview
        
        self.title = "Options"
        Utils.center_window(self)
        self.focus()

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side='top',  fill='both',  padx=10,  pady=5)
        self.top_bar = ttk.Frame(self.top_frame,  width=180,  height=185)
        self.top_bar.grid(row=2,  column=0,  padx=5,  pady=5)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side='bottom',  fill='both',  padx=10,  pady=5)
        self.bottom_bar = ttk.Frame(self.bottom_frame,  width=180,  height=185)
        self.bottom_bar.grid(row=2,  column=0,  padx=5,  pady=5)

        # Create a Label messages widget
        self.label_messages = ttk.Label(
            self.bottom_bar,
            text=""
        )

        # Widgets openssh config
        self.strvar_openssh = tk.StringVar()
        self.strvar_openssh.set(Utils.option_get("general", "path_openssh_config", self.label_messages))
        self.entry_openssh = ttk.Entry(
            self.top_bar,
            width=60,
            textvariable=self.strvar_openssh
        ).grid(row=1, column=0,  padx=5,  pady=5)
        self.btn_openssh = ttk.Button(
            self.top_bar,
            text="Search OpenSSH config",
            width=30,
            command=self.search_openssh_config
        ).grid(row=1,  column=1,  padx=5,  pady=5)

        # Widgets winscp
        self.strvar_winscp = tk.StringVar()
        self.strvar_winscp.set(Utils.option_get("general", "path_winscp_exe", self.label_messages))
        self.entry_winscp = ttk.Entry(
            self.top_bar,
            width=60,
            textvariable=self.strvar_winscp
        ).grid(row=2,  column=0,  padx=5,  pady=5)
        self.btn_winscp = ttk.Button(
            self.top_bar,
            text="Search WinSCP executable",
            width=30,
            command=self.search_winscp_exec
        ).grid(row=2,  column=1,  padx=5,  pady=5)

        # Widgets WSL distro
        self.strvar_combo = tk.StringVar()
        self.strvar_combo.set(Utils.option_get("general", "wsl_distro", self.label_messages))
        self.combo_wsl = ttk.Combobox(
            self.top_bar,
            width=60,
            state="readonly",
            values=Utils.get_wsl_distros(self.label_messages),
            textvariable=self.strvar_combo
        ).grid(row=3,  column=0,  padx=5,  pady=5)

        self.label_combo=ttk.Label(
            self.top_bar,
            text="Select a WSL distribution"
        ).grid(row=3,  column=1,  padx=5,  pady=5)

        # Create button "Save"
        ttk.Button(
            self.bottom_bar,
            text="Guardar",
            width=20,
            command=self.save_changes
        ).grid(row=1,  column=1,  padx=5,  pady=5)

        self.transient(self.master)
        self.grab_set()
        self.wait_window(self)
