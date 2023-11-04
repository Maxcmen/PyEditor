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
            side="left",
            fill="y",
            padx=10,
            pady=10,
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
