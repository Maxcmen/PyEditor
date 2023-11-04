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
