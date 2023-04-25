from configupdater import ConfigUpdater
import os
import subprocess
import configparser

configfile_name = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + "\RemoteHelper.ini"

class Utils():

    def open_terminal(m_label, hostname, ip, port, user_name, key):
        try:
            wsl_distro = Utils.option_get("general", "wsl_distro", m_label)
            terminal_command = [
                "wt",
                "-w",
                "0",
                "-p",
                "Command Prompt",
                "--title",
                hostname,
                "wsl.exe",
                "-d",
                wsl_distro,
                "ssh",
                "-o",
                "StrictHostKeyChecking=no",
                "-i",
                key,
                "-p",
                str(port),
                user_name + "@" + ip
            ]
            subprocess.Popen(terminal_command)
        except Exception as e:
            print(e)
            m_label("Error running Terminal app")

    def open_winscp(m_label, ip, port, user_name, key):
        try:
            path_winscp = Utils.option_get("general", "path_winscp_exe", m_label)        
            # if os.path.isfile(os.getenv('LOCALAPPDATA') + "\Programs\WinSCP\WinSCP.exe"):
            #     path_winscp = os.getenv('LOCALAPPDATA') + "\Programs\WinSCP\WinSCP.exe"
            # elif os.path.isfile(os.getenv('PROGRAMFILES') + "\WinSCP\WinSCP.exe"):
            #     path_winscp = os.getenv('PROGRAMFILES') + "\WinSCP\WinSCP.exe"
            # elif os.path.isfile(os.getenv('PROGRAMFILES(X86)') + "\WinSCP\WinSCP.exe"):
            #     path_winscp = os.getenv('PROGRAMFILES(X86)') + "\WinSCP\WinSCP.exe"
            if path_winscp == "None":
                m_label("Error!!!: WinSCP not found")
            else:
                winscp_command = [
                    path_winscp,
                    "sftp://" + user_name + "@" + ip + ":" + str(port),
                    "/privatekey=" + key
                ]    
                subprocess.Popen(winscp_command)
        except Exception as e:
            print(e)
            m_label("Error running WinSCP app")

    def option_set(section, option, value):
        if not os.path.exists(configfile_name):
            open(configfile_name, 'w').close()
        Config = ConfigUpdater()
        Config.read(configfile_name)
        if not Config.has_section(section):
            Config.add_section(section)
        Config[section][option] = value
        Config.update_file()

    def option_get(section, option, label):
        value = "None"
        try:
            config = configparser.ConfigParser()
            config.read(configfile_name)
            value = config[section][option]
        except:
            label.config(text="Error reading config file")
    
        return value

    def get_wsl_distros(label):
        distros = []
        try:
            output = subprocess.run(['wsl.exe', '-l', '--all', '-q'], capture_output=True)
            for line in output.stdout.decode("UTF-16").split('\n'):
                if not len(line) == 0:
                    distros.append(line)

        except Exception as e:
            label.config(text="Error getting WSL distros")
            print(e)

        return distros
    
    def center_window(self):
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/3 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight/2)
        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
