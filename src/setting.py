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

style = "darkly"

WIDTH = 1920
HEIGHT = 1080

title = "PyEditor"

size = (
    int(WIDTH / 1.25),
    HEIGHT - 100,
)

alpha = 1.0

font = ""
fontsize = 14

encode = "utf-8"

pythonVersion = f"{sys.version_info[0]}.{sys.version_info[1]}"
pythonPath = sys.executable


def loadConfig():
    settings = \
        [
            "style",
            "WIDTH",
            "HEIGHT",
            "title",
            "alpha",
            "font",
            "fontsize",
            "encode",
        ]

    with open(
            "config",
            "r",
            "utf-8"
        ) as f:
        config = eval(
            f.read()
        )

        for setting in config:
            if setting in settings:
                globals()[
                    setting
                ] = config[
                    setting
                ]


try:
    loadConfig()
except:
    pass
