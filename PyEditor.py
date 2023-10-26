import builtins
import keyword
import os
import re
import sys
import subprocess
import threading
import tkinter

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
global pythonPath

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
pythonPath = sys.executable


class CMDProcess(threading.Thread):
    def __init__(
        self, args, callback
    ):
        """
        初始化函数，创建一个线程对象，继承自threading.Thread类。
        
        Args:
            args: 命令行参数列表，类型为List[str]。
            callback: 回调函数，类型为Callable。
        
        Returns:
            None
        
        """
        threading.Thread.__init__(
            self
        )

        self.args = args
        self.callback = callback
        self.cwd = "./"

    def run(self):
        """
        运行给定的命令参数，并在有回调函数的情况下，将命令输出的每一行传递给回调函数处理。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
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
        """
        初始化函数，创建文件资源管理器窗口的界面布局。
        
        Args:
            master: 窗口的顶部部件。
            path: 文件路径。
        
        Returns:
            None.
        """
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
        """
        Pop out the menu of directory or file.
        
        Args:
            event: The event which triggers the pop out menu.
        
        Returns:
            None.
        
        """
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
        """
        从文件系统中删除选定的文件。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
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
        """
        重命名文件
        
        Args:
            无
        
        Returns:
            无
        """
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
        """
        创建文件夹。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
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
        
        """
        创建一个新文件
        
        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        """
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
        """
        打开文件夹，更新目录树。
        
        Args:
            path (str): 文件夹路径。
        
        Returns:
            None.
        
        """
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
        """
        加载指定路径下的所有文件，并以树形结构展示文件目录
        
        Args:
            parent: 父节点路径
            path: 文件目录路径
        
        Returns:
            None
        """
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
        """
        获取路径最后的文件名或文件夹名
        
        Args:
            path (str): 文件或文件夹的路径
        
        Returns:
            str: 文件名或文件夹名
        """
        """获取路径最后的文件名或文件夹名"""
        pathList = os.path.split(
            path
        )
        return pathList[-1]


def configure_tags(
    text_widget, tags
):
    """
    为给定的文本控件配置标签。
    
    Args:
        text_widget (Text): 需要配置标签的文本控件。
        tags (Dict[str, str]): 包含标签名和对应颜色的字典。
    
    Returns:
        None.
    """
   
    for tag, color in tags.items():
        text_widget.tag_delete(tag)
        text_widget.tag_config(
            tag, foreground=color
        )


def group(*choices):
    """
    拼接给定字符串列表并返回一个正则表达式的匹配组。
    
    Args:
        choices (str): 需要拼接的字符串列表。
    
    Returns:
        str: 拼接后的字符串，并在前后加上括号，用于正则表达式分组。
    """
    return (
        "("
        + "|".join(choices)
        + ")"
    )


def any(*choices):
    """
    返回一个匹配多个选择项的正则表达式。
    
    Args:
        *choices (str): 多个选择项，可以是单个字符或字符串。
    
    Returns:
        str: 包含多个选择项的正则表达式，以"*"结尾。
    
    """
    return group(*choices) + "*"


def maybe(*choices):
    """
    返回一个表示可能性的字符串，其中包含给定选项的组合以及一个问号。
    
    Args:
        choices: 一个或多个字符串的元组，表示可能的选项。
    
    Returns:
        一个字符串，其中包含所有选项的组合以及一个问号。
    
    """
    return group(*choices) + "?"


def _compile(expr):
    """
    根据表达式字符串编译正则表达式对象。
    
    Args:
        expr (str): 表达式字符串。
    
    Returns:
        re.Pattern: 编译后的正则表达式对象。
    
    """
    return re.compile(
        expr, re.UNICODE
    )


def on_key_release(text_widget):
    """
    对给定的文本widget进行关键字、字符串、注释、变量、数字等的语法高亮
    
    Args:
        text_widget: 待高亮的文本widget
    
    Returns:
        None
    """
    lines = text_widget.get(
        1.0, ttk.END
    ).splitlines()

    # regular expressions for number, string and keywords
    Hexnumber = (
        r"0[xX](?:_?[0-9a-fA-F])+"
    )
    Binnumber = r"0[bB](?:_?[01])+"
    Octnumber = (
        r"0[oO](?:_?[0-7])+"
    )
    Decnumber = r"(?:0(?:_?0)*|[1-9](?:_?[0-9])*)"
    Intnumber = group(
        Hexnumber,
        Binnumber,
        Octnumber,
        Decnumber,
    )
    Exponent = r"[eE][-+]?[0-9](?:_?[0-9])*"
    Pointfloat = group(
        r"[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?",
        r"\.[0-9](?:_?[0-9])*",
    ) + maybe(Exponent)
    Expfloat = (
        r"[0-9](?:_?[0-9])*"
        + Exponent
    )
    Floatnumber = group(
        Pointfloat, Expfloat
    )
    Imagnumber = group(
        r"[0-9](?:_?[0-9])*[jJ]",
        Floatnumber + r"[jJ]",
    )
    Number = group(
        Imagnumber,
        Floatnumber,
        Intnumber,
    )

    String1 = (
        r"\'([^\\\n]|(\\.))*?\'"
    )
    String2 = (
        r"\"([^\\\n]|(\\.))*?\""
    )
    String = group(
        String1, String2
    )

    Comment = r"#.*"

    Variable = (
        r"[a-z][a-zA-Z0-9_]*"
    )

    regex = re.compile(
        r"(^\s*"
        r"(?P<if>if|elif|else)"
        + "|"  # if condition
        r"(?P<for>for|while)"
        + "|"  # for loop
        r"(?P<import>import|from|as)"
        + "|"
        r"(?P<keywords>def|class|lambda|try|except|pass|with|as)"  # keywords
        rf"|(?P<number>{Number})"
        rf"|(?P<string>{String})"
        rf"|(?P<comment>{Comment})"
        rf"|(?P<variable>{Variable})"
        r"[\s\(]+)"
    )
    for idx, line in enumerate(
        lines
    ):
        keywords_tag = (
            f"keywords_{idx}"
        )
        for_tag = f"for_{idx}"
        if_tag = f"if_{idx}"
        import_tag = (
            f"import_{idx}"
        )
        number_tag = (
            f"number_{idx}"
        )
        string_tag = (
            f"string_{idx}"
        )
        comment_tag = (
            f"comment_{idx}"
        )
        variable_tag = (
            f"variable_{idx}"
        )

        tags = {
            keywords_tag: "blue",
            for_tag: "#FFA500",
            if_tag: "#FFA500",
            import_tag: "#FFA500",
            number_tag: "purple",
            string_tag: "green",
            comment_tag: "green",
            variable_tag: "purple"
            # add new tag here
        }
        configure_tags(
            text_widget, tags
        )

        for (
            match
        ) in regex.finditer(line):
            for tag in tags:
                group_name = (
                    tag.split("_")[
                        0
                    ]
                )
                try:
                    if (
                        -1
                        != match.start(
                            group_name
                        )
                    ):
                        text_widget.tag_add(
                            tag,
                            "{0}.{1}".format(
                                idx
                                + 1,
                                match.start(
                                    group_name
                                ),
                            ),
                            "{0}.{1}".format(
                                idx
                                + 1,
                                match.end(
                                    group_name
                                ),
                            ),
                        )
                except:
                    pass


class Autocomplete:
    def __init__(
        self, parent, text_widget
    ):
        """
        Args:
            parent: 包含文本框的父窗口
            text_widget: 绑定键盘释放事件的文本框
        
        Returns:
            None
        
        """
        self.text_widget = (
            text_widget
        )
        self.text_widget.bind(
            "<KeyRelease>",
            self.on_keyrelease,
        )

        self.listbox = (
            tkinter.Listbox(parent)
        )
        self.listbox.pack(
            side="right", fill="y"
        )

        self.autocomplete_keywords = keyword.kwlist + dir(
            builtins
        )

    def on_keyrelease(self, event):
        """
        当按键释放事件发生时，该函数会被调用。
        
        Args:
            event: 按键释放事件对象。
        
        Returns:
            None.
        
        """
        if (
            event.keysym
            == "Return"
        ):  # ignore return key
            return
        # get current line text
        (
            line_number,
            column,
        ) = self.text_widget.index(
            "insert"
        ).split(
            "."
        )
        current_line = (
            self.text_widget.get(
                f"{line_number}.0",
                "insert",
            )
        )
        if (
            current_line
        ):  # if there is text on current line
            token = (
                current_line.split(
                    " "
                )[-1]
            )
            token = token.split(
                "."
            )[-1]
            self.update_listbox(
                token
            )

    def update_listbox(self, line):
        """
        更新自动补全列表框，根据输入的行进行匹配并显示在列表框中。
        
        Args:
            line (str): 用户输入的字符串。
        
        Returns:
            None.
        
        """
        self.listbox.delete(
            0, "end"
        )  # clear the listbox
        for (
            word
        ) in (
            self.autocomplete_keywords
        ):
            if word.startswith(
                line
            ):
                self.listbox.insert(
                    "end", word
                )  # insert matching word into listbox
        self.listbox.bind(
            "<<ListboxSelect>>",
            self.on_listbox_select,
        )  # bind event

    def on_listbox_select(
        self, event
    ):
        """
        Args:
            event: Tkinter 的 Listbox 事件对象
        
        Returns:
            None
        
        """
        try:
            widget = event.widget
            selection = (
                widget.curselection()
            )
            selected_word = (
                widget.get(
                    selection[0]
                )
            )
            # delete current line
            (
                line_number,
                _,
            ) = self.text_widget.index(
                "insert"
            ).split(
                "."
            )
            self.text_widget.delete(
                f"{line_number}.0",
                "insert",
            )
            # insert selected word
            self.text_widget.insert(
                "insert",
                selected_word,
            )
        except:
            return


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

        a = self.Editors[
            selected_tab
        ]

        pass

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
            line_numbers.yview(*xx)
            Text.yview(*xx)

        def Wheel(event):
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

        Text = ttk.Text(CodeEditor)

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

        Text.see(ttk.END)

        Text.configure(
            yscrollcommand=scrollbar.set
        )

        Autocomplete(
            CodeEditor, Text
        )

        Text.pack(
            side="top", fill="both"
        )

        Text.config(
            font=(font, fontsize)
        )

        Text.insert(1.0, text)

        on_key_release(Text)

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
            无返回值，仅弹出一个对话框显示PyEditor的版本号和开发者信息
        
        """
        Messagebox.okcancel(
            title="PyEditor",
            message="版本: 0.16 \n开发者: 郑翊 & 王若同",
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


if __name__ == "__main__":
    Editor()
