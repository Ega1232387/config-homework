import argparse
import os
import shutil
import tarfile
import datetime
import tkinter as tk


class ShellEmulator:
    def __init__(self, file):
        self.username = "invertie"
        self.fs_archive = file
        self.fs_structure = {}  # Хранит файлы и каталоги виртуальной файловой системы
        self.current_directory = ""  # Текущая директория внутри виртуальной файловой системы
        self.log_actions = []
        self.load_virtual_fs()  # Загружаем виртуальную файловую систему при инициализации

    def load_virtual_fs(self):
        if not os.path.exists(self.fs_archive):
            print(f"Archive {self.fs_archive} not found.")
            exit(1)

        # Загружаем файловую систему в память, используя tarfile
        with tarfile.open(self.fs_archive, 'r') as tar:
            for member in tar:
                if member.isdir():
                    self.fs_structure[member.name] = set()
                elif member.isfile():
                    file_content = tar.extractfile(member).read().decode()
                    self.fs_structure[member.name] = file_content

        self.fs_structure[''] = set()
        for member in self.fs_structure:
            if member == '':
                continue

            if member.count('/') == 0:
                self.fs_structure[''].add(member)

            if type(self.fs_structure[member]) != set:
                continue

            for smember in self.fs_structure:
                if smember.startswith(member) and member.count('/') + 1 == smember.count('/'):
                    self.fs_structure[member].add(os.path.basename(smember))

    def log_action(self, action):
        self.log_actions.append((datetime.datetime.now(), action))

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return "Unknown command"

        cmd = parts[0]
        self.log_action(command)  # Логируем команду

        if cmd == "ls":
            return self.cmd_ls()
        elif cmd == "cd":
            return self.cmd_cd(parts[1] if len(parts) > 1 else "")
        elif cmd == "exit":
            return "Exiting..."
        elif cmd == "rm":
            return self.cmd_rm(parts[1] if len(parts) > 1 else "")
        elif cmd == "clear":
            return self.cmd_clear()
        elif cmd == "whoami":
            return self.cmd_whoami()
        else:
            return "Unknown command"

    def cmd_ls(self):
        path = self.current_directory if self.current_directory in self.fs_structure else ""
        if path in self.fs_structure:
            if type(self.fs_structure[path]) == set:
                return "\n".join(self.fs_structure[path])
            else:
                return "Not a directory"
        else:
            return "Directory not found"

    def cmd_cd(self, path):
        if path == "..":
            new_path = os.path.dirname(self.current_directory)
        else:
            new_path = os.path.join(self.current_directory, path)

        if new_path in self.fs_structure and type(self.fs_structure[new_path]) == set:
            self.current_directory = new_path
            return f"Changed directory to {self.current_directory}"
        else:
            return f"Directory {path} not found"

    def cmd_rm(self, filename):
        file_path = os.path.join(self.current_directory, filename).replace("\\", "/")
        if file_path in self.fs_structure:
            with tarfile.open(self.fs_archive, 'r') as tar:
                with tarfile.open("temp_" + self.fs_archive, 'w') as tar_out:
                    for tarinfo in tar:
                        if tarinfo.path != file_path:
                            temp_file = tar.extractfile(tarinfo)
                            tar_out.addfile(tarinfo, temp_file)
            shutil.copyfile("temp_" + self.fs_archive, self.fs_archive)
            os.remove("temp_" + self.fs_archive)
            self.fs_structure = {}
            self.load_virtual_fs()
            return f"File {filename} removed"
        else:
            return f"File {filename} not found"

    def cmd_clear(self):
        return "clr↑"

    def cmd_whoami(self):
        return self.username

def run():
    global input_area, result, output_area
    result = emulator.execute_command(input_area.get("1.0", tk.END)[2:-1])
    input_area.delete("1.0", tk.END)
    input_area.insert(tk.END, "$ ")
    if result == "clr↑":
        output_area.delete('1.0', tk.END)
    elif result == "Exiting...":
        exit()
    else:
        output_area.insert(tk.END, result + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор командной строки")
    parser.add_argument('-f', '--file', required=True, help="Путь к архиву файловой системы")
    result = ""
    args = parser.parse_args()
    emulator = ShellEmulator(args.file)
    root = tk.Tk()
    root.title("GUI")
    output_area = tk.Text(root, height=20, width=100)
    output_area.pack(pady=10)
    input_area = tk.Text(root, height=5, width=100)
    input_area.pack(pady=10)
    copy_button = tk.Button(root, text="Enter", command=run)
    copy_button.pack(pady=5)
    input_area.insert(tk.END, "$ ")
    root.mainloop()