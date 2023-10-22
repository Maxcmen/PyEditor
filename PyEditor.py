import os
import sys
import subprocess
import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import (
    PhotoImage,
    filedialog,
)
from ttkbootstrap.dialogs import (
    Messagebox,
)
from ttkbootstrap.dialogs import (
    Querybox,
)
import idlelib.colorizer as idc
import idlelib.percolator as idp


# Setting
global style
global WIDTH
global HEIGHT
global title
global size
global alpha

global font
global fontsize

global encode

global pythonVersion

style = "litera"

WIDTH = 1920
HEIGHT = 1080

title = "PyEditor"

size = (
    int(WIDTH / 1.25),
    HEIGHT - 100,
)

alpha = 0.95

font = ""
fontsize = 14

encode = "utf-8"

pythonVersion = f"{sys.version_info[0]}.{sys.version_info[1]}"


class CMDProcess(threading.Thread):
    def __init__(
        self, args, callback
    ):
        threading.Thread.__init__(
            self
        )

        self.args = args
        self.callback = callback
        self.cwd = "./"

    def run(self):
        """运行命令"""
        self.proc = subprocess.Popen(
            self.args,
            bufsize=1,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=self.cwd,
        )

        while (
            self.proc.poll()
            is None
        ):
            line = (
                self.proc.stdout.readline()
            )  # 获取输出缓冲区

            self.proc.stdout.flush()

            if self.callback:
                self.callback(
                    line
                )  # 调用打印函数


class TreeWindow(ttk.Frame):
    def __init__(
        self, master, path
    ):
        self.rootPath = path

        self.frame = ttk.Frame(
            master
        )

        self.frame.pack(
            side="left", fill="y"
        )

        self.label = ttk.Label(
            self.frame,
            text="文件资源管理器",
        )

        self.label.pack(
            anchor="nw"
        )
        self.label.config(
            font=("黑体", 8)
        )

        self.tree = ttk.Treeview(
            self.frame
        )

        self.tree.pack(
            side="left", fill="y"
        )

        self.filepaths = {
            self.getlastPath(
                path
            ): path
        }

        root = self.tree.insert(
            "",
            "end",
            text=self.getlastPath(
                path
            ),
            open=True,
        )

        self.loadTree(root, path)

        # 当前选择文件夹显示的菜单
        self.dirpopOutMenu = (
            ttk.Menu(self.frame)
        )

        self.dirpopOutMenu.add_command(
            label="新建文件",
            command=self.createFile,
        )
        self.dirpopOutMenu.add_command(
            label="新建文件夹",
            command=self.createDir,
        )

        self.dirpopOutMenu.add_separator()

        self.dirpopOutMenu.add_command(
            label="重命名",
            command=self.reName,
        )

        self.dirpopOutMenu.add_separator()

        self.dirpopOutMenu.add_command(
            label="删除",
            command=self.delFile,
        )

        # 当前选择文件显示的菜单
        self.filepopOutMenu = (
            ttk.Menu(self.frame)
        )

        self.filepopOutMenu.add_command(
            label="重命名",
            command=self.reName,
        )
        self.filepopOutMenu.add_command(
            label="删除",
            command=self.delFile,
        )

        # self.filepopOutMenu.add_separator()

        # self.filepopOutMenu.add_command(label="复制绝对路径")
        # self.filepopOutMenu.add_command(label="复制相对路径")

        self.tree.bind(
            "<Button-3>",
            self.popOut,
        )

    def popOut(self, event):
        selected_item = (
            self.tree.selection()[
                0
            ]
            if len(
                self.tree.selection()
            )
            else ""
        )
        values = self.tree.item(
            selected_item
        )

        if values["text"] == "":
            return

        if os.path.isdir(
            self.filepaths[
                values["text"]
            ]
        ):
            # Dir popOutMenu if now is dir
            self.dirpopOutMenu.post(
                event.x_root,
                event.y_root,
            )

        else:
            # File PopOutMenu else
            self.filepopOutMenu.post(
                event.x_root,
                event.y_root,
            )

        self.frame.update()

    def delFile(self):
        """删除文件"""
        if Messagebox.yesno(
            message="确定删除吗?"
        ):
            selected_item = self.tree.selection()[
                0
            ]
            values = (
                self.tree.item(
                    selected_item
                )
            )

            path = self.filepaths[
                values["text"]
            ]

            os.remove(path)

            self.OpenDir(
                self.rootPath
            )

    def reName(self):
        """重命名文件"""

        # 获取当前选择节点
        selected_item = (
            self.tree.selection()[
                0
            ]
        )
        values = self.tree.item(
            selected_item
        )

        if (
            values["text"] == ""
        ):  # 为空返回
            return

        path = self.filepaths[
            values["text"]
        ]

        newName = Querybox.get_string(
            title="PyEditor",
            prompt="请输入文件的新名称",
            initialvalue="NewName",
        )

        if (
            newName == ""
            or os.path.split(path)[
                0
            ]
        ):
            return

        newPath = os.path.join(
            os.path.split(path)[0],
            newName,
        )

        os.rename(path, newPath)

        self.OpenDir(
            self.rootPath
        )  # 刷新资源管理器

    def createDir(self):
        """创建文件夹"""
        selected_item = (
            self.tree.selection()[
                0
            ]
        )
        values = self.tree.item(
            selected_item
        )

        path = self.filepaths[
            values["text"]
        ]

        dirName = Querybox.get_string(
            title="PyEditor",
            prompt="请输入文件夹名称:",
            initialvalue="NewDir",
        )

        if dirName != "":
            dirPath = os.path.join(
                path, dirName
            )

            if not os.path.exists(
                dirPath
            ):
                os.mkdir(dirPath)

                self.OpenDir(
                    self.rootPath
                )

    def createFile(self):
        """新建文件"""
        selected_item = (
            self.tree.selection()[
                0
            ]
        )
        values = self.tree.item(
            selected_item
        )

        path = self.filepaths[
            values["text"]
        ]

        dirName = Querybox.get_string(
            title="PyEditor",
            prompt="请输入文件名称:",
            initialvalue="NewFile",
        )

        if dirName != "":
            filePath = (
                os.path.join(
                    path, dirName
                )
            )

            if not os.path.exists(
                filePath
            ):
                with open(
                    filePath, "a+"
                ) as f:
                    pass

                self.OpenDir(
                    self.rootPath
                )

    def OpenDir(self, path):
        """打开文件夹"""
        self.rootPath = (
            path  # 刷新根目录
        )

        self.tree.delete(
            *self.tree.get_children()
        )  # 删除当前所以节点

        root = self.tree.insert(
            "",
            "end",
            text=self.getlastPath(
                path
            ),
            open=True,
        )

        self.loadTree(root, path)

    def loadTree(
        self, parent, path
    ):
        """加载节点"""
        for filepath in os.listdir(
            path
        ):
            abs = os.path.join(
                path, filepath
            )

            treey = self.tree.insert(
                parent,
                "end",
                text=self.getlastPath(
                    filepath
                ),
            )

            self.filepaths[
                self.getlastPath(
                    filepath
                )
            ] = abs

            if os.path.isdir(abs):
                self.loadTree(
                    treey, abs
                )  # 递归创建文件树

    def getlastPath(self, path):
        """获取路径最后的文件名或文件夹名"""
        pathList = os.path.split(
            path
        )
        return pathList[-1]


class Editor:
    def __init__(self):
        self.style = style

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.title = "PyEditor"

        self.themename = style

        self.size = size

        self.minsize = (0, 0)
        self.maxsize = (1920, 1080)

        self.resizable = None
        self.alpha = alpha

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

        self.root.iconbitmap(
            "favicon.ico"
        )

        self.root.place_window_center()

        # Menu
        self.menu = ttk.Menu(
            self.root
        )

        # file menu
        self.fileMenu = ttk.Menu(
            self.menu
        )

        self.menu.add_cascade(
            label="文件",
            menu=self.fileMenu,
        )

        self.fileMenu.add_command(
            label="新建文件",
            command=self.newFile,
        )
        self.fileMenu.add_command(
            label="打开文件",
            command=self.openFile,
        )

        self.fileMenu.add_command(
            label="打开文件夹",
            command=self.openDir,
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="关闭文件",
            command=self.exitFile,
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="保存",
            command=self.save,
        )
        self.fileMenu.add_command(
            label="另存为",
            command=self.saveAs,
        )

        self.fileMenu.add_separator()

        self.fileMenu.add_command(
            label="退出",
            command=self.exit,
        )

        # edit menu
        self.editMenu = ttk.Menu(
            self.menu
        )

        self.menu.add_cascade(
            label="编辑",
            menu=self.editMenu,
        )

        self.editMenu.add_command(
            label="撤销",
            command=self.backout,
        )
        self.editMenu.add_command(
            label="恢复",
            command=self.regain,
        )

        self.editMenu.add_separator()

        self.editMenu.add_command(
            label="复制",
            command=self.copy,
        )
        self.editMenu.add_command(
            label="粘贴",
            command=self.paste,
        )
        self.editMenu.add_command(
            label="剪切",
            command=self.cut,
        )

        # self.editMenu.add_command(label="查找", command=self.find)
        # self.editMenu.add_command(label="替换", command=self.replace)

        # run menu
        self.runMenu = ttk.Menu(
            self.menu
        )

        self.menu.add_cascade(
            label="运行",
            menu=self.runMenu,
        )

        self.runMenu.add_command(
            label="运行",
            command=self.runFile,
        )
        self.runMenu.add_command(
            label="停止运行",
            command=self.stopRun,
        )

        # help Menu
        self.helpMenu = ttk.Menu(
            self.menu
        )

        self.menu.add_cascade(
            label="帮助",
            menu=self.helpMenu,
        )

        self.helpMenu.add_command(
            label="关于",
            command=self.about,
        )

        # file Tree
        self.path = os.getcwd()

        self.fileTree = TreeWindow(
            self.root, self.path
        )

        self.fileTree.tree.bind(
            "<<TreeviewSelect>>",
            self.fileTreeClick,
        )  # 绑定 “当节点被选择事件”

        self.status = f"0:0  CRLF  {encode}  Python {pythonVersion}"

        self.statusBar = ttk.Frame(
            self.root
        )
        self.statusBar.pack(
            side="bottom", fill="x"
        )

        self.statusLabel = (
            ttk.Label(
                self.statusBar,
                text=self.status,
                font=("", 12),
            )
        )
        self.statusLabel.pack(
            side="right"
        )

        self.nowFilePath = (
            ttk.Label(
                self.statusBar,
                font=("", 12),
            )
        )
        self.nowFilePath.pack(
            side="left"
        )

        # Code Text
        self.codeEditor = (
            ttk.Notebook(self.root)
        )

        self.Editors = (
            {}
        )  # 保存每个编辑界面，标签页名为key
        self.Editors[
            "untitled"
        ] = self.createEditor(
            self.root
        )

        self.codeEditor.add(
            self.Editors[
                "untitled"
            ],
            text="untitled",
        )

        self.codeEditor.pack(
            fill=ttk.BOTH,
            expand=True,
        )

        # PopoutMenu
        self.popOutMenu = ttk.Menu(
            self.root
        )

        self.popOutMenu.add_cascade(
            label="运行",
            command=self.runMenu,
        )
        self.popOutMenu.add_cascade(
            label="停止运行",
            command=self.stopRun,
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="关闭文件",
            command=self.exitFile,
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_cascade(
            label="保存",
            command=self.save,
        )
        self.popOutMenu.add_cascade(
            label="另存为",
            command=self.saveAs,
        )
        self.popOutMenu.add_cascade(
            label="全部保存",
            command=self.saveAll,
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="撤销",
            command=self.backout,
        )
        self.popOutMenu.add_command(
            label="恢复",
            command=self.regain,
        )

        self.popOutMenu.add_separator()

        self.popOutMenu.add_command(
            label="复制",
            command=self.copy,
        )
        self.popOutMenu.add_command(
            label="粘贴",
            command=self.paste,
        )
        self.popOutMenu.add_command(
            label="剪切",
            command=self.cut,
        )

        self.root.bind(
            "<Button-3>",
            self.popout,
        )

        self.filepaths = {}

        self.root.after(
            10, self.updateStatus
        )

        self.root.config(
            menu=self.menu
        )

        self.root.mainloop()

    def updateStatus(self):
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        index = (
            self.Editors[
                selected_tab
            ]
            .children["!frame2"]
            .children[
                "!scrolledtext"
            ]
            .index(ttk.INSERT)
        )

        index = index.replace(
            ".", ":"
        )  # 将点换成冒号

        self.status = f"{index} CRLF {encode} Python {pythonVersion}"

        self.statusLabel[
            "text"
        ] = self.status
        self.statusLabel.update()

        if (
            selected_tab
            in self.filepaths
        ):
            self.nowFilePath[
                "text"
            ] = " > ".join(
                os.path.split(
                    self.filepaths[
                        selected_tab
                    ]
                )
            )
        else:
            self.nowFilePath[
                "text"
            ] = "untitled"
        self.nowFilePath.update()

        self.root.after(
            10, self.updateStatus
        )  # 调用自己实现循环

    def fileTreeClick(self, event):
        """当资源管理器中的文件树节点被选择且为文件时打开"""
        selected_item = (
            self.fileTree.tree.selection()[
                0
            ]
            if len(
                self.fileTree.tree.selection()
            )
            else ""
        )
        values = self.fileTree.tree.item(
            selected_item
        )

        if values == "":
            return

        if not os.path.isdir(
            self.fileTree.filepaths[
                values["text"]
            ]
        ):
            self.openFile(
                filepath=self.fileTree.filepaths[
                    values["text"]
                ]
            )

    def createEditor(
        self,
        root,
        text="",
        type="python",
    ):
        """创建一个文件编辑界面"""
        CodeEditor = ttk.Frame(
            root
        )

        buttonFrame = ttk.Frame(
            CodeEditor
        )

        buttonFrame.pack(
            anchor="ne", fill="x"
        )

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

        exitButton.pack(
            side="right"
        )

        # 类型为python时才需要
        if type == "python":
            stopButton.pack(
                side="right"
            )
            runButton.pack(
                side="right"
            )

        Text = ttk.ScrolledText(
            CodeEditor
        )

        Text.see(ttk.END)

        Text.pack(
            side="top", fill="both"
        )

        Text.config(
            font=(font, fontsize)
        )

        Text.insert(1.0, text)

        # 类型为python时才需要
        if type == "python":
            idc.color_config(
                Text
            )  # 高亮显示

            p = idp.Percolator(
                Text
            )
            d = (
                idc.ColorDelegator()
            )
            p.insertfilter(d)

            runWindow = (
                ttk.ScrolledText(
                    CodeEditor
                )
            )

            runWindow.pack(
                side="bottom",
                fill="x",
            )

            runWindow.config(
                font=("黑体", 14)
            )

        return CodeEditor

    def pictureViewer(
        self, root, path
    ):
        """创建一个图片查看器"""
        image = ttk.Label(
            root,
            image=ttk.PhotoImage(
                False, file=path
            ),
        )

        image.pack()

        exitButton = ttk.Button(
            root,
            text="✖",
            bootstyle="danger",
            command=self.exitFile,
        )

        exitButton.pack(
            anchor="ne"
        )

        return image

    def saveAll(self):
        """保存所有文件"""
        for (
            filepath
        ) in self.Editors.keys():
            self.save(
                filepath=filepath
            )

    def exitFile(self):
        """关闭标签页"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )
        )

        self.codeEditor.forget(
            index
        )

    def popout(self, event):
        """右键菜单"""
        self.popOutMenu.post(
            event.x_root,
            event.y_root,
        )
        self.root.update()

    def openDir(self):
        """打开文件夹"""
        dirPath = (
            filedialog.askdirectory()
        )  # 查询文件夹路径

        if dirPath == "":
            return

        self.fileTree.OpenDir(
            dirPath
        )

        self.root.update()

    def about(self):
        """获取帮助信息"""
        Messagebox.okcancel(
            title="PyEditor",
            message="版本: 0.11 \n开发者: 郑翊 & 王若同",
        )

    def newFile(self):
        """创建新文件"""
        max = 0

        # 因为前面都为untitled，后面则是数字，以此分辨
        for (
            name
        ) in self.Editors.keys():
            if (
                name[:8]
                == "untitled"
                and len(name) != 8
            ):
                index = 8 - len(
                    name
                )
                if max < int(
                    name[index:]
                ):
                    max = int(
                        name[
                            index:
                        ]
                    )

        max += 1

        self.Editors[
            f"untitled{max}"
        ] = self.createEditor(
            self.root
        )

        self.codeEditor.add(
            self.Editors[
                f"untitled{max}"
            ],
            text=f"untitled{max}",
        )

    def openFile(
        self, filepath=""
    ):
        """打开文件"""
        for (
            path
        ) in self.Editors.keys():
            if path == filepath:
                return

        if filepath == "":
            filepath = (
                filedialog.askopenfilename()
            )  # 获取文件路径

        if filepath == "":
            return

        filename = os.path.split(
            filepath
        )[-1]

        text = ""
        type = (
            "python"
            if filename.split(".")[
                -1
            ]
            in ("py", "python")
            else ""
        )

        with open(
            filepath, "rb"
        ) as f:
            text = f.read()

            try:
                text = text.decode(
                    encode
                )
            except (
                UnicodeDecodeError
            ):  # 解密失败
                if not filename.split(
                    "."
                )[
                    -1
                ] in (
                    "png",
                    "jpg",
                ):
                    Messagebox.okcancel(
                        title="PyEditor",
                        message="解码失败!",
                    )

        if filename.split(".")[
            -1
        ] in (
            "png",
            "jpg",
        ):
            self.Editors[
                filepath
            ] = self.pictureViewer(
                root=self.root,
                path=filepath,
            )
        else:
            self.Editors[
                filename
            ] = self.createEditor(
                self.root,
                text=text,
                type=type,
            )

        self.codeEditor.add(
            self.Editors[filename],
            text=filename,
        )

        self.filepaths[
            filename
        ] = filepath

    def backout(self):
        """撤销文本框编辑"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[  # 这个元素访问方式......
            "!frame"  # 调试慢慢找到的......
        ].children[
            "!scrolledtext"
        ].edit_undo()

    def regain(self):
        """恢复编辑框编辑"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[
            "!frame"
        ].children[
            "!scrolledtext"
        ].edit_redo()

    def save(self):
        """保存文件"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        if len(selected_tab) >= 8:
            if (
                selected_tab[:8]
                == "untitled"
            ):
                self.saveAs()  # 未命名的文件需要另存为
        else:
            with open(
                self.filepaths[
                    selected_tab
                ],
                "wb+",
            ) as f:
                f.write(
                    self.Editors[
                        selected_tab
                    ]
                    .children[
                        "!frame2"
                    ]
                    .children[
                        "!scrolledtext"
                    ]
                    .get(
                        1.0,
                        ttk.END,
                    )
                    .encode(encode)
                )

                Messagebox.okcancel(
                    title="PyEditor",
                    message="保存成功",
                )

    def saveAs(self):
        """另存为文件"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        filepath = (
            filedialog.askopenfilename()
        )  # 获取另存为路径

        if filepath == "":
            return

        with open(
            filepath, "wb+"
        ) as f:
            f.write(
                self.Editors[
                    self.filepaths[
                        selected_tab
                    ]
                ]
                .children["!frame"]
                .children[
                    "!scrolledtext"
                ]
                .get(1.0, ttk.END)
                .encode(encode)
            )

        Messagebox.okcancel(
            title="PyEditor",
            message="保存成功",
        )

        self.exitFile()
        self.openFile(filepath)

    def copy(self):
        """复制"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[
            "!frame"
        ].children[
            "!scrolledtext"
        ].event_generate(  # 生成一个复制事件
            "<<Copy>>"
        )

    def paste(self):
        """粘贴"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[
            "!frame"
        ].children[
            "!scrolledtext"
        ].event_generate(  # 创建一个粘贴事件
            "<<Paste>>"
        )

    def cut(self):
        """剪切"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[
            "!frame"
        ].children[
            "!scrolledtext"
        ].event_generate(
            "<<Cut>>"
        )

    def exit(self):
        """退出编辑器"""
        sys.exit()

    def runFile(self):
        """运行文件"""
        self.stopRun()

        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.save()  # 运行前先保存

        cmd = [
            "python",
            "-u",
            self.filepaths[
                selected_tab
            ],
        ]  # 运行命令

        testProcess = CMDProcess(
            cmd,
            lambda info: self.Editors[
                selected_tab
            ]
            .children["!frame3"]
            .children[
                "!scrolledtext"
            ]
            .insert(ttk.END, info),
        )
        testProcess.start()

    def stopRun(self):
        """停止运行"""
        index = (
            self.codeEditor.index(
                "current"
            )
        )
        selected_tab = (
            self.codeEditor.tab(
                index
            )["text"]
        )

        self.Editors[
            selected_tab
        ].children[
            "!frame3"
        ].children[
            "!scrolledtext"
        ].delete(
            1.0, ttk.END
        )


if __name__ == "__main__":
    Editor()
