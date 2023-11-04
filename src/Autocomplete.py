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
        self.parent = parent

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
            x,
            y,
        ) = (
            self.text_widget.winfo_pointerxy()
        )
        win_x, win_y = (
            self.parent.winfo_rootx(),
            self.parent.winfo_rooty(),
        )

        x, y = x - win_x, y - win_y

        self.listbox.place(
            x=x, y=y
        )
        self.listbox.update()

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
        当选择框（ListBox）发生选择事件时，将选中的单词插入到文本框（Text）中并删除当前行文本。

        Args:
            event: Tkinter 的 Listbox 事件对象，用于获取选择框（ListBox）的相关信息。

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
