import os
import sys

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage, filedialog
from ttkbootstrap.dialogs import Messagebox
import idlelib.colorizer as idc
import idlelib.percolator as idp

from RunCmd import CMDProcess
from TreeWindow import TreeWindow


class Editor:
    def __init__(self):
        self.style = "superhero"

        self.WIDTH = 1920
        self.HEIGHT = 1080

        self.title = "PyEditor"

        self.themename = self.style

        self.size = (
            int(self.WIDTH / 1.25),
            self.HEIGHT - 50,
        )
        self.minsize = (0, 0)
        self.maxsize = (1920, 1080)

        self.resizable = None
        self.alpha = 1.0

        # root
        self.root = ttk.Window(
            title=self.title,
            themename=self.themename,
            size=self.size,
            minsize=self.minsize,
            maxsize=self.maxsize,
            resizable=self.resizable,
            alpha=self.alpha,
        )

        self.root.place_window_center()

        # Menu
        self.menu = ttk.Menu(self.root)

        # file menu
        self.fileMenu = ttk.Menu(self.menu)

        self.menu.add_cascade(
            label="文件", menu=self.fileMenu
        )

        self.fileMenu.add_command(
            label="新建文件", command=self.newFile
        )
        self.fileMenu.add_command(
            label="打开文件", command=self.openFile
        )

        self.fileMenu.add_command(
            label="打开文件夹", command=self.openDir
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="关闭文件", command=self.exitFile
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="保存", command=self.save
        )
        self.fileMenu.add_command(
            label="另存为", command=self.saveAs
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="退出", command=self.exit
        )

        # edit menu
        self.editMenu = ttk.Menu(self.menu)

        self.menu.add_cascade(
            label="编辑", menu=self.editMenu
        )

        self.editMenu.add_command(
            label="撤销", command=self.backout
        )
        self.editMenu.add_command(
            label="恢复", command=self.regain
        )

        self.editMenu.add_separator()

        self.editMenu.add_command(
            label="复制", command=self.copy
        )
        self.editMenu.add_command(
            label="粘贴", command=self.paste
        )
        self.editMenu.add_command(
            label="剪切", command=self.cut
        )

        # self.editMenu.add_command(label="查找", command=self.find)
        # self.editMenu.add_command(label="替换", command=self.replace)

        # run menu
        self.runMenu = ttk.Menu(self.menu)

        self.menu.add_cascade(label="运行", menu=self.runMenu)

        self.runMenu.add_command(
            label="运行", command=self.runFile
        )
        self.runMenu.add_command(
            label="停止运行", command=self.stopRun
        )

        # help Menu
        self.helpMenu = ttk.Menu(self.menu)

        self.menu.add_cascade(
            label="帮助", menu=self.helpMenu
        )

        self.helpMenu.add_command(
            label="关于", command=self.about
        )

        # file Tree
        self.path = os.getcwd()

        self.fileTree = TreeWindow(self.root, self.path)

        self.fileTree.tree.bind(
            "<<TreeviewSelect>>", self.fileTreeClick
        )

        # Code Text
        self.codeEditor = ttk.Notebook(self.root)

        self.Editors = {}
        self.Editors["untitled"] = self.createEditor(
            self.root
        )

        self.codeEditor.add(
            self.Editors["untitled"], text="untitled"
        )

        self.codeEditor.pack(fill=ttk.BOTH, expand=True)

        # PopoutMenu
        self.popOutMenu = ttk.Menu(self.root)

        self.popOutMenu.add_cascade(
            label="运行", command=self.runMenu
        )
        self.popOutMenu.add_cascade(
            label="停止运行", command=self.stopRun
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="关闭文件", command=self.exitFile
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_cascade(
            label="保存", command=self.save
        )
        self.popOutMenu.add_cascade(
            label="另存为", command=self.saveAs
        )
        self.popOutMenu.add_cascade(
            label="全部保存", command=self.saveAll
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="撤销", command=self.backout
        )
        self.popOutMenu.add_command(
            label="恢复", command=self.regain
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="复制", command=self.copy
        )
        self.popOutMenu.add_command(
            label="粘贴", command=self.paste
        )
        self.popOutMenu.add_command(
            label="剪切", command=self.cut
        )

        self.root.bind("<Button-3>", self.popout)

        self.fileTreepopOutMenu = ttk.Menu(self.root)

        self.fileTreepopOutMenu.add_cascade(label="新建文件")
        self.fileTreepopOutMenu.add_cascade(label="新建文件夹")

        self.fileTreepopOutMenu.add_separator()

        self.fileTreepopOutMenu.add_cascade(label="重命名")
        self.fileTreepopOutMenu.add_cascade(label="删除")

        self.fileTree.tree.bind(
            "<Button-3>", self.fileTreepopOut
        )

        self.root.config(menu=self.menu)

        self.root.mainloop()

    def fileTreepopOut(self, event):
        self.fileTreepopOutMenu.post(
            event.x_root, event.y_root
        )
        self.root.update()

    def fileTreeClick(self, event):
        selected_item = self.fileTree.tree.selection()[0]
        values = self.fileTree.tree.item(selected_item)

        if not os.path.isdir(
            self.fileTree.filepaths[values["text"]]
        ):
            self.openFile(
                filepath=self.fileTree.filepaths[
                    values["text"]
                ]
            )

    def createEditor(self, root, text="", type="python"):
        CodeEditor = ttk.Frame(root)

        buttonFrame = ttk.Frame(CodeEditor, style="dark")

        buttonFrame.pack(anchor="ne", fill="x")

        runButton = ttk.Button(
            buttonFrame,
            text="▶",
            bootstyle="success",
            command=self.runFile,
        )
        stopButton = ttk.Button(
            buttonFrame,
            text="■",
            bootstyle="danger",
            command=self.stopRun,
        )

        exitButton = ttk.Button(
            buttonFrame,
            text="✖",
            bootstyle="danger",
            command=self.exitFile,
        )

        exitButton.pack(side="right")

        if type == "python":
            stopButton.pack(side="right")
            runButton.pack(side="right")

        Text = ttk.ScrolledText(CodeEditor)

        Text.see(ttk.END)

        Text.pack(side="top", fill="x")

        Text.config(font=("黑体", 14))

        Text.insert(1.0, text)

        if type == "python":
            idc.color_config(Text)

            p = idp.Percolator(Text)
            d = idc.ColorDelegator()
            p.insertfilter(d)

        runWindow = ttk.ScrolledText(CodeEditor)

        runWindow.pack(side="bottom", fill="x")

        runWindow.config(font=("黑体", 14))

        return CodeEditor

    def saveAll(self):
        for filepath in self.Editors.keys():
            self.save(filepath=filepath)

    def exitFile(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)

        self.codeEditor.forget(index)

    def popout(self, event):
        self.popOutMenu.post(event.x_root, event.y_root)
        self.root.update()

    def openDir(self):
        dirPath = filedialog.askdirectory()

        if dirPath == "":
            return

        self.fileTree.OpenDir(dirPath)

        self.root.update()

    def about(self):
        Messagebox.okcancel(
            title="PyEditor",
            message="版本: 0.04 \n开发者: 郑翊 & 王若同",
        )

    def newFile(self):
        max = 0

        for name in self.Editors.keys():
            if name[:8] == "untitled" and len(name) != 8:
                index = 8 - len(name)
                if max < int(name[index:]):
                    max = int(name[index:])

        max += 1

        self.Editors[f"untitled{max}"] = self.createEditor(
            self.root
        )
        self.codeEditor.add(
            self.Editors[f"untitled{max}"],
            text=f"untitled{max}",
        )

    def openFile(self, filepath=""):
        for path in self.Editors.keys():
            if path == filepath:
                return

        if filepath == "":
            filepath = filedialog.askopenfilename()
        filename = filepath.split("/")[-1]

        text = ""
        type = (
            "python"
            if filename.split(".")[-1] in ("py", "python")
            else ""
        )

        with open(filepath, "rb+") as f:
            text = f.read().decode("utf-8")

        self.Editors[filepath] = self.createEditor(
            self.root, text=text, type=type
        )
        self.Editors[filepath]

        self.codeEditor.add(
            self.Editors[filepath], text=filepath
        )

    def backout(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame"
        ].children["!scrolledtext"].edit_undo()

    def regain(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame"
        ].children["!scrolledtext"].edit_redo()

    def save(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        if len(selected_tab) >= 8:
            if selected_tab[:8] == "untitled":
                self.saveAs()
            else:
                with open(selected_tab, "wb+") as f:
                    f.write(
                        self.Editors[selected_tab]
                        .children["!frame"]
                        .children["!scrolledtext"]
                        .get(1.0, ttk.END)
                        .encode("utf-8")
                    )

        Messagebox.okcancel(
            title="PyEditor", message="保存成功"
        )

    def saveAs(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        filepath = filedialog.askopenfilename()

        if filepath == "":
            return

        with open(filepath, "wb+") as f:
            f.write(
                self.Editors[selected_tab]
                .children["!frame"]
                .children["!scrolledtext"]
                .get(1.0, ttk.END)
                .encode("utf-8")
            )

        Messagebox.okcancel(
            title="PyEditor", message="保存成功"
        )

        self.exitFile()
        self.openFile(filepath)

    def copy(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame"
        ].children["!scrolledtext"].event_generate(
            "<<Copy>>"
        )

    def paste(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame"
        ].children["!scrolledtext"].event_generate(
            "<<Paste>>"
        )

    def cut(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame"
        ].children["!scrolledtext"].event_generate(
            "<<Cut>>"
        )

    def exit(self):
        sys.exit()

    def runFile(self):
        self.stopRun()

        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.save()

        cmd = ["python", "-u", selected_tab]

        testProcess = CMDProcess(
            cmd,
            lambda info: self.Editors[selected_tab]
            .children["!frame2"]
            .children["!scrolledtext"]
            .insert(ttk.END, info),
        )
        testProcess.start()

    def stopRun(self):
        index = self.codeEditor.index("current")
        selected_tab = self.codeEditor.tab(index)["text"]

        self.Editors[selected_tab].children[
            "!frame2"
        ].children["!scrolledtext"].delete(1.0, ttk.END)


Editor()
