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
