# Overview

I Work with Ansible in [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux), my `./ssh/config` file has the connection
data to all the serves that I manage, this tool reads that file and show a grid with all the hosts and give the possibility to
stablish a SSH session using the Windows [Terminal](https://github.com/microsoft/terminal) and a SFTP session
using [WinSCP](https://winscp.net/eng/index.php) by clicking in a button.

# TODO

- Improve configuration of widgets (frames, layout (grid, pack))
- Add function to search in the treeview data, something like [this](https://www.youtube.com/watch?v=WdhNkabUAVU)

# Development

My machine has de following software installed:

- Windows 11
- Python 3.10
- WSL 2 + Ubuntu 22.04

## Configure local environment

```
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

# Links

## Windows

- https://pureinfotech.com/list-environment-variables-windows-10/
- https://superuser.com/questions/1704004/how-to-open-multiple-tabs-and-run-ssh-from-the-command-line-in-windows-ternimal

## PyInstaller

- https://pyinstaller.org/en/stable/usage.html#general-options
- https://www.pythonguis.com/tutorials/packaging-tkinter-applications-windows-pyinstaller/

## tkinter

- https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV
- https://www.youtube.com/playlist?list=PLd1leK7rsaC_JaF8bC4Knn1OHVm9zqJSJ
