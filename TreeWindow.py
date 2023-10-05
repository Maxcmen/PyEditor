import tkinter
import ttkbootstrap as ttk
import os


class TreeWindow(ttk.Frame):
    def __init__(self, master, path):
        self.frame = ttk.Frame(master)

        self.frame.pack(side="left", fill="y")

        self.label = ttk.Label(self.frame, text="文件资源管理器")

        self.label.pack(anchor="nw")
        self.label.config(font=("黑体", 8))

        self.tree = ttk.Treeview(self.frame)

        self.tree.pack(side="left", fill="y")

        self.filepaths = {self.getlastPath(path): path}

        root = self.tree.insert(
            "",
            "end",
            text=self.getlastPath(path),
            open=True,
        )

        self.loadTree(root, path)

    def OpenDir(self, path):
        self.tree.delete(*self.tree.get_children())

        root = self.tree.insert(
            "",
            "end",
            text=self.getlastPath(path),
            open=True,
        )

        self.loadTree(root, path)

    def loadTree(self, parent, path):
        for filepath in os.listdir(path):
            abs = os.path.join(path, filepath)

            treey = self.tree.insert(
                parent,
                "end",
                text=self.getlastPath(filepath),
            )

            self.filepaths[self.getlastPath(filepath)] = abs

            if os.path.isdir(abs):
                self.loadTree(treey, abs)

    def getlastPath(self, path):
        pathList = os.path.split(path)
        return pathList[-1]
