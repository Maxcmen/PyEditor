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

import plugins


class Plugins:
    def __init__(
        self, parent, pads
    ):
        """
        初始化插件窗口

        Args:
            parent: 父窗口
            pads: 插件列表

        Returns:
            None

        """
        self.parent = parent
        self.pads = pads

        self.pluginsWindow = (
            ttk.Toplevel(parent)
        )

        self.pluginsList = ttk.Treeview(
            self.pluginsWindow,
            columns=(
                "name",
                "version",
                "introduce",
            ),
            show="headings",
            displaycolumns="#all",
        )

        self.pluginsList.heading(
            "name",
            text="名字",
            anchor="w",
        )
        self.pluginsList.heading(
            "version",
            text="版本",
            anchor="w",
        )
        self.pluginsList.heading(
            "introduce",
            text="介绍",
            anchor="w",
        )

        for (
            plugin
        ) in plugins.plugins:
            self.pluginsList.insert(
                "",
                "end",
                values=plugin[:3],
            )

        self.pluginsList.pack(
            fill="both"
        )

        self.pluginsList.bind(
            "<<TreeviewSelect>>",
            self.on_select,
        )

        self.pluginsWindow.title(
            "插件"
        )

        self.pluginsWindow.mainloop()

    def on_select(self, event):
        """
        Args:
            event: 事件对象，本函数不使用

        Returns:
            None

        功能：在插件列表被选中时运行，根据选中的插件名称查找对应插件，启动插件进程或添加插件界面到pads列表。

        """
        foc = (
            self.pluginsList.focus()
        )
        val = self.pluginsList.set(
            foc
        )

        for (
            plugin
        ) in plugins.plugins:
            if (
                plugin[0]
                == val["name"]
            ):
                if (
                    plugin[3]
                    == False
                ):
                    p = Process(
                        target=plugin[
                            -1
                        ]
                    )
                    p.start()

                    return

                else:
                    plugin = plugin[
                        -1
                    ](
                        self.parent
                    ).frame
                self.pads.add(
                    plugin,
                    text=val[
                        "name"
                    ],
                )
