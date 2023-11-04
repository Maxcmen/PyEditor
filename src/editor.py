import builtins
import ctypes
import keyword
import os
import re
import sys
import subprocess
import tempfile
import threading
import tkinter
from multiprocessing import Process
from tkinter.ttk import Style

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

from .Autocomplete import *
from .cmdprocess import *
from .highlighting import *
from .treewindow import *
from .setting import *


class Editor:
    def __init__(self):
        """
        初始化窗口，菜单栏，以及代码编辑器等组件

        Args:
            无

        Returns:
            无
        """
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
            resizable=self.resizable,
            alpha=self.alpha,
        )

        self.root.iconbitmap(
            "res/favicon.ico"
        )

        self.root.place_window_center()

        self.Menubutton = (
            ttk.Menubutton(
                self.root, text="≡"
            )
        )
        self.Menubutton.pack(
            anchor="nw"
        )

        # Menu
        self.menu = ttk.Menu(
            self.Menubutton
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

        # view Menu
        self.viewMenu = ttk.Menu(
            self.menu
        )

        self.menu.add_cascade(
            label="视图",
            menu=self.viewMenu,
        )

        self.themeMenu = ttk.Menu(
            self.menu
        )

        self.themeMenu.add_command(
            label="Darkly",
            command=lambda: self.switchTheme(
                style="darkly"
            ),
        )

        self.themeMenu.add_command(
            label="Superhero",
            command=lambda: self.switchTheme(
                style="superhero"
            ),
        )

        self.themeMenu.add_command(
            label="Cyborg",
            command=lambda: self.switchTheme(
                style="cyborg"
            ),
        )

        self.themeMenu.add_command(
            label="Cosmo",
            command=lambda: self.switchTheme(
                style="cosmo"
            ),
        )

        self.themeMenu.add_command(
            label="Litera",
            command=lambda: self.switchTheme(
                style="litera"
            ),
        )

        self.viewMenu.add_cascade(
            label="主题",
            menu=self.themeMenu,
        )

        self.menu.add_command(
            label="插件",
            command=self.PluginsMarket,
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

        self.Menubutton.config(
            menu=self.menu
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
            padx=10,
            pady=10,
        )

        self.codeEditor.bind(
            "<Button-3>",
            self.padpopout,
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

        self.padPopOutMenu = (
            ttk.Menu(self.root)
        )

        self.padPopOutMenu.add_command(
            label="新建页面",
            command=self.newFile,
        )

        self.padPopOutMenu.add_command(
            label="关闭页面",
            command=self.exitFile,
        )

        self.filepaths = {}

        self.root.after(
            10, self.updateStatus
        )

        self.root.config()

        self.root.mainloop()

    def PluginsMarket(self):
        """
        打开插件市场。
        Args:
            无参数。
        Returns:
            无返回值。
        """
        Plugins(
            self.root,
            self.codeEditor,
        )

    def switchTheme(self, style):
        """
        切换应用主题。

        Args:
            style: str类型，可选，应用主题样式名称。

        Returns:
            无返回值。

        """
        self.root.style.theme_use(
            style
        )

        self.root.update()

    def updateStatus(self):
        """
        更新状态栏显示的信息，包括光标所在位置和当前文件路径。

        Args:
            无参数。

        Returns:
            无返回值。

        """
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

        try:
            a = self.Editors[
                selected_tab
            ]
        except KeyError:
            return

        index = (
            self.Editors[
                selected_tab
            ]
            .children["!text"]
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
        """
        当资源管理器中的文件树节点被选择且为文件时打开

        Args:
            event: 事件对象，此处未使用

        Returns:
            None
        """
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
        """
        创建一个文件编辑界面

        Args:
            root: 界面所在的Tkinter窗口
            text: 编辑器默认文本内容
            type: 编辑器类型，目前只支持"python"

        Returns:
            Tkinter中的Frame对象，包含编辑器界面
        """
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

        # 更新行号显示

        def update_line_numbers(
            event=None,
        ):
            """
            更新文本编辑器的行号。

            Args:
                event: 触发该函数的事件对象，可选。

            Returns:
                无返回值。

            """
            line_numbers.config(
                state=ttk.NORMAL
            )
            line_numbers.delete(
                "1.0", ttk.END
            )

            # 获取当前文本编辑器内容的行数
            line_count = (
                Text.get(
                    "1.0", "end"
                ).count("\n")
                + 1
            )

            # 插入行号
            for i in range(
                1, line_count + 1
            ):
                line_numbers.insert(
                    ttk.END,
                    f"{i}\n",
                )

            line_numbers.config(
                state=ttk.DISABLED
            )
            line_numbers.configure(
                yscrollcommand=scrollbar.set
            )

        def scollerbarCommand(*xx):
            """
            该函数实现滚动条命令的功能，接收参数xx，并将其传递给line_numbers和Text的yview方法

            Args:
                xx: 接收任意个参数，表示滚动条的滚动位置

            Returns:
                None
            """
            line_numbers.yview(*xx)
            Text.yview(*xx)

        def Wheel(event):
            """
            滚动事件处理函数，用于处理鼠标滚轮事件。

            Args:
                event: 鼠标滚轮事件对象。

            Returns:
                None。
            """
            Text.yview_scroll(
                int(
                    -1
                    * (
                        event.delta
                        / 120
                    )
                ),
                "units",
            )
            line_numbers.yview_scroll(
                int(
                    -1
                    * (
                        event.delta
                        / 120
                    )
                ),
                "units",
            )

        Text = ttk.Text(
            CodeEditor, tabs=56
        )

        line_numbers = ttk.Text(
            CodeEditor,
            width=4,
            padx=4,
            pady=4,
            takefocus=0,
            border=0,
            background="lightgrey",
            state=ttk.DISABLED,
            font=(font, fontsize),
        )

        line_numbers.pack(
            side="left", fill="y"
        )

        scrollbar = ttk.Scrollbar(
            CodeEditor,
            command=scollerbarCommand,
        )
        scrollbar.pack(
            side=ttk.RIGHT,
            fill="y",
        )

        if type == "python":
            Autocomplete(
                CodeEditor, Text
            )

        Text.see(ttk.END)

        Text.configure(
            yscrollcommand=scrollbar.set
        )

        Text.pack(
            side="top", fill="both"
        )

        Text.config(
            font=(font, fontsize)
        )

        Text.insert(1.0, text)

        Text.bind(
            "<Key>",
            update_line_numbers,
        )

        Text.bind(
            "<MouseWheel>", Wheel
        )
        line_numbers.bind(
            "<MouseWheel>", Wheel
        )

        update_line_numbers()

        # 类型为python时才需要
        if type == "python":
            on_key_release(Text)

            Text.bind(
                "<Key>",
                lambda event: on_key_release(
                    Text
                ),
            )

            runWindow = ttk.Text(
                CodeEditor
            )

            runWindow.pack(
                side="bottom",
                fill="x",
            )

            runWindow.config(
                font=("黑体", 14)
            )

        Text.bind(
            "<Button-3>",
            self.popout,
        )

        return CodeEditor

    def pictureViewer(
        self, root, path
    ):
        """
        创建一个图片查看器

        Args:
            root: 图片查看器的顶层窗口
            path: 图片文件的路径

        Returns:
            image: Label控件，显示图片
        """
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
        """
        保存所有文件。

        Args:
            无参数。

        Returns:
            无返回值。

        """
        """保存所有文件"""
        for (
            filepath
        ) in self.Editors.keys():
            self.save(
                filepath=filepath
            )

    def exitFile(self):
        """
        关闭当前选中的文件标签页

        Args:
            无

        Returns:
            无

        """
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

    def padpopout(self, event):
        """
        显示右键菜单

        Args:
            event: 触发鼠标事件的对象

        Returns:
            None
        """
        self.padPopOutMenu.post(
            event.x_root,
            event.y_root,
        )
        self.root.update()

    def popout(self, event):
        """
        显示右键菜单

        Args:
            event: 触发鼠标事件的对象

        Returns:
            None
        """
        self.popOutMenu.post(
            event.x_root,
            event.y_root,
        )
        self.root.update()

    def openDir(self):
        """
        打开文件夹

        Args:
            无

        Returns:
            无

        """
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
        """
        获取关于PyEditor的帮助信息

        Args:
            无参数

        Returns:
            无返回值
            ，仅弹出一个对话框显示PyEditor的版本号和开发者信息

        """
        Messagebox.okcancel(
            title="PyEditor",
            message="版本: 0.23 \n开发者: 郑翊 & 王若同",
        )

    def newFile(self):
        """
        创建新文件并将其添加到编辑器中。

        Args:
            无参数。

        Returns:
            无返回值，仅在 self.Editors 中添加新编辑器。

        """
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
        """
        打开文件

        Args:
            filepath (str, optional): 文件路径. Defaults to "".

        Returns:
            None
        """
        """打开文件"""
        for (
            path
        ) in self.Editors.keys():
            try:
                if (
                    self.filepaths[
                        path
                    ]
                    == filepath
                ):
                    return
            except:
                pass

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
        """
        撤销文本框编辑。

        Args:
            无。

        Returns:
            无返回值。

        """
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
            "!text"  # 调试慢慢找到的......
        ].edit_undo()

    def regain(self):
        """
        恢复编辑框编辑

        Args:
            无参数

        Returns:
            无返回值
        """
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
            "!text"
        ].edit_redo()

    def save(self):
        """
        保存文件

        Args:
            无

        Returns:
            无
        """
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
                        "!text"
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
        """
        另存为文件

        Args:
            无

        Returns:
            无

        Raises:
            无
        """
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
                    selected_tab
                ]
                .children["!text"]
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
        """复制当前选中的文本内容

        Args:
            无

        Returns:
            无
        """
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
            "!text"
        ].event_generate(  # 生成一个复制事件
            "<<Copy>>"
        )

    def paste(self):
        """
        在选定的编辑器中执行粘贴操作。

        Args:
            无。

        Returns:
            无返回值。

        """
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
            "!text"
        ].event_generate(  # 创建一个粘贴事件
            "<<Paste>>"
        )

    def cut(self):
        """
        剪切当前选中的文本。

        Args:
            无参数。

        Returns:
            无返回值。

        """
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
            "!text"
        ].event_generate(
            "<<Cut>>"
        )

    def exit(self):
        """
        退出编辑器

        Args:
            无

        Returns:
            无

        """
        """退出编辑器"""
        sys.exit()

    def runFile(self):
        """
        运行文件

        Args:
            无

        Returns:
            无
        """
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
            pythonPath,
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
            .children["!text2"]
            .insert(ttk.END, info),
        )
        testProcess.start()

    def stopRun(self):
        """
        停止运行

        Args:
            无

        Returns:
            无
        """
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
            "!text2"
        ].delete(
            1.0, ttk.END
        )
