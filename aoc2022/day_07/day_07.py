# Solution of AOC2022 day 7

import tools
from typing import Dict
import re


class File:
    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    def name(self):
        return self._name

    def size(self):
        return self._size


class Directory:
    def __init__(
        self,
        name: str,
        parent: "Directory" = None,
        directories: Dict[str, "Directory"] = None,
        files: Dict[str, File] = None,
    ):
        self._name = name
        self._parent = parent
        self._directories = directories or dict()
        self._files = files or dict()

    def add_file(self, file: File):
        self._files[file.name()] = file

    def add_directory(self, directory: "Directory"):
        self._directories[directory.name()] = directory

    def remove_directory(self, name: str):
        del self._directories[name]

    def name(self):
        return self._name

    def parent(self):
        if not self._parent:
            raise RuntimeError("Root direcory has no parent")
        return self._parent

    def files(self):
        return self._files

    def directories(self):
        return self._directories

    def size(self):
        files_size = sum(f.size() for f in self.files().values())
        dirs_size = sum(d.size() for d in self.directories().values())
        return files_size + dirs_size

    def output(self):
        sorted_entries = list(sorted(list(self.directories().keys()) + list(self.files().keys())))

        s = ""
        for name in sorted_entries:
            if name in self.directories():
                s += f"dir {name}\n"
            if name in self.files():
                s += f"{self.files()[name].size()} {name}\n"

        for _, d in self.directories().items():
            s += f"$ cd {d.name()}\n$ ls\n"
            s += d.output()
            s += "$ cd ..\n"
        return s

    def to_str(self, level = 0):
        pre = "".join(["  "] * level)
        s = f"{pre}+ DIR  {self.name()} {self.size()}\n"
        for _, f in self.files().items():
            s += f"{pre}  - FILE {f.name()} {f.size()}\n"
        for _, d in self.directories().items():
            s += d.to_str(level + 1)
        return s

    def __repr__(self):
        s = self.to_str()
        return s


class Path:
    def __init__(self, path=None):
        self._path = path or list()

    def cd_in(self, directory: str):
        self._path.append(directory)

    def cd_out(self):
        if len(self._path):
            self._path.pop()
        else:
            raise RuntimeError("Already at root")

    def __repr__(self):
        return "/" + "/".join(self._path)


if __name__ == "__main__":
    data = tools.read_input_file(__file__)[1:]

    files = list()
    directories = list()

    def create_directory(cmd: str, parent: str):
        m = re.match("dir (.+)", cmd)
        return Directory(m.group(1), parent, dict(), dict())

    def create_file(cmd: str):
        m = re.match("(\\d+) (.+)", cmd)
        return File(m.group(2), int(m.group(1)))

    root = Directory("/", None)
    directories.append(root)
    cwd = root
    path = Path()

    i = 0
    while i < len(data):
        if data[i] == "$ ls":
            i = i + 1
            while "$" not in data[i]:
                if data[i][0:3] == "dir":
                    d = create_directory(data[i], cwd)
                    cwd.add_directory(d)
                    directories.append(d)
                else:
                    f = create_file(data[i])
                    cwd.add_file(f)
                    files.append(f)
                i = i + 1
                if i >= len(data):
                    break
        elif "$ cd" in data[i]:
            m = re.match("\\$ cd (.+)", data[i])
            token = m.group(1)
            if token == "..":
                path.cd_out()
                cwd = cwd.parent()
            else:
                path.cd_in(token)
                cwd = cwd.directories()[token]
            i = i + 1
        else:
            raise RuntimeError(f"Unknown command: {data[i]}")

    dir_sizes = [d.size() for d in directories]

    from functools import cmp_to_key
    dirs_sorted = sorted(directories, key = cmp_to_key(lambda d1, d2: d1.size() - d2.size()))

    small_dirs = list(filter(lambda d: d.size() <= 100000, directories))
    small_dirs_size = sum(d.size() for d in small_dirs)
    # [print(d.name(), d.size()) for d in small_dirs]
    print(small_dirs_size)

    space_needed = root.size() - 40000000
    dirs_to_delete = sorted(list(filter(lambda d: d.size() >= space_needed, directories)), key = cmp_to_key(lambda d1, d2: d1.size() - d2.size()))
    print(dirs_to_delete[0].size())
