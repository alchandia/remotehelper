# Purpose

I Work with Ansible and my file `./ssh/config` has the connection data to all the serves that I manage, this tool reads that file and show a grid with all the hosts and give the possibility to stablish a SSH session using gnome-terminal and a SFTP session using Filezilla by clicking in a button.

# Install

The installer will create a directory in `$HOME/bin` and then a symlink to the script, if you `$PATH` include the directory `$HOME/bin` you will be able to run the helper using the command `remotehelper`

```
chmod 755 installer.sh
./installer.sh
```

# Configuration/To-Do/Problems

- The first time you open a SFTP session you need to add manually the key file `$HOME/.ssh/filezilla` in the option `Edit` -> `Settings` -> `SFTP` of Filezilla. This key is a symlink to the key file associated with the current selected host. Every time you select other host and click the button `SFTP` this symlink is updated
- If you open the application using a desktop shortcut, every time you open a SSH session a new gnome terminal if open. If you want to open all the sessions in the same gnome-terminal windows, you need to open the aplication using a gnome terminal.

# Links

- https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html
- https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBBnHFDEANbv9q8T4CONGZE