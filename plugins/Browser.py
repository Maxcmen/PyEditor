import sys

try:
    from cefpython3 import cefpython as cef
except: pass

import tkinter as tk
import platform

WINDOWS = (
    platform.system() == "Windows"
)
LINUX = (
    platform.system() == "Linux"
)
MAC = platform.system() == "Darwin"
# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

cef.Initialize()  # init


class Browser(tk.Frame):
    class LoadHandler(object):
        def __init__(
            self, browser
        ):
            """
            Args:
                browser: 浏览器实例对象

            Returns:
                None

            """
            self.browser = browser

        def OnBeforePopup(
            self, target_url, **a
        ):
            """
            Args:
                target_url (str): 目标网址
                **a: 其他参数

            Returns:
                bool: 是否阻止弹出窗口

            """
            res = self.browser.NewWindow(
                target_url
            )
            if res == "break":
                return True

    class FocusHandler(object):
        "From cefpython3.example.tkinter_"

        def __init__(
            self, browser_frame
        ):
            """
            Args:
                browser_frame: 一个对象，表示浏览器窗口的框架。

            Returns:
                None.

            """
            self.browser_frame = (
                browser_frame
            )

        def OnSetFocus(
            self, source, **_
        ):
            """
            Args:
                source: 获取焦点的控件
                **_: 未使用的关键字参数，用于后续扩展功能

            Returns:
                bool: 返回False，表示焦点设置失败；返回True，表示焦点设置成功。
            """
            return False

        def OnGotFocus(self, **_):
            """
            当窗口获得焦点时调用，用于修复CEF焦点问题（#255）。调用浏览器窗口的focus_set方法，
            以摆脱URL输入框内的光标类型。

            Args:
                **_: 捕获任意数量的非关键字参数，此处未使用。

            Returns:
                无返回值。

            """

            self.browser_frame.focus_set()

    def __init__(
        self, *a, url="", **b
    ):
        """初始化函数，创建一个cef的浏览器窗口并绑定相关处理器

        Args:
            *a: 父类构造函数的参数
            url: 浏览器窗口打开的网址，默认为"https://www.baidu.com/"
            **b: 父类构造函数的参数字典

        Returns:
            None

        Raises:
            无异常。如果创建浏览器失败，则抛出AssertionError异常。

        Usage:
            class MyWindow(CEFWindow):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.create_browser("https://www.example.com/")
        """
        super().__init__(*a, **b)
        # 创建浏览器
        # create browser
        window_info = (
            cef.WindowInfo()
        )
        # 获取窗口信息
        rect = [
            0,
            0,
            self.winfo_width(),
            self.winfo_height(),
        ]
        # 设置窗口矩形
        window_info.SetAsChild(
            self.get_window_handle(),
            rect,
        )
        if not url:
            url = "https://www.baidu.com/"
        # 创建浏览器，同步创建
        self.browser = (
            cef.CreateBrowserSync(
                window_info,
                url=url,
            )
        )
        assert self.browser
        # 设置客户端处理器，加载处理器和焦点处理器
        self.browser.SetClientHandler(
            self.LoadHandler(self)
        )
        self.browser.SetClientHandler(
            self.FocusHandler(self)
        )
        # 绑定配置事件，当窗口大小改变时触发 _configure 方法，以适应框架大小变化
        # fit frame
        self.bind(
            "<Configure>",
            self._configure,
        )

    def _configure(self, event):
        """
        根据事件中的宽度和高度信息，调整窗口或视口的大小。

        Args:
            event: tkinter.Event对象，包含事件发生的详细信息，包括宽度和高度信息。

        Returns:
            None
        """

        res = self.event_generate(
            "<<Configure>>"
        )
        if res == "break":
            return
        width = event.width
        height = event.height
        if WINDOWS:
            WindowUtils.OnSize(
                self.winfo_id(),
                0,
                0,
                0,
            )
        elif LINUX:
            self.browser.SetBounds(
                0, 0, width, height
            )
        self.browser.NotifyMoveOrResizeStarted()

    def NewWindow(self, url):
        """
        打开一个新的浏览器窗口并加载指定的URL。

        Args:
            url (str): 要加载的URL地址。

        Returns:
            str: 返回一个字符串 "break"。

        """
        self.load(url)
        return "break"

    def loadurl(self, url):
        """
        加载指定URL。

        Args:
            url (str): 要加载的URL。

        Returns:
            None
        """
        self.browser.StopLoad()
        self.browser.LoadUrl(url)

    def geturl(self):
        """
        获取当前浏览器页面的URL。

        Args:
            无参数。

        Returns:
            str: 当前浏览器页面的URL。

        """
        return (
            self.browser.GetUrl()
        )

    def reload(self):
        """
        刷新当前浏览器页面。

        Args:
            无。

        Returns:
            无返回值。

        """
        self.browser.Reload()

    def get_window_handle(self):
        """
        获取窗口句柄。

        Args:
            无。

        Returns:
            int: 窗口句柄的整数值。

        Raises:
            Exception: 如果无法获取窗口句柄，则抛出异常。

        注：
            该函数是从 cef 模块中引入的。
        """
        "From cef"
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import (
                NSApp,
            )

            # noinspection PyUnresolvedReferences
            import objc

            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(
                NSApp.windows()[
                    -1
                ].contentView()
            )
        else:
            raise Exception(
                "Couldn't obtain window handle"
            )


def maincefloop(n=200):
    """
    该函数用于启动CEF的消息循环，并在指定的时间间隔内重复执行。

    Args:
        n (int): 消息循环的执行间隔，单位为毫秒。默认为200。

    Returns:
        None
    """
    cef.MessageLoopWork()
    tk._default_root.after(
        n, maincefloop, n
    )


def bye():
    """
    关闭CEF浏览器进程。

    Args:
        无参数。

    Returns:
        无返回值。

    """
    cef.Shutdown()


def test():
    """
    主函数入口

    Args:
        无

    Returns:
        None
    """

    def makenew(url):
        """
        该函数用于打开一个链接并创建一个新的浏览器实例

        Args:
            url: str类型，表示需要打开的链接

        Returns:
            None

        """
        b = Browser(note, url=url)
        note.add(
            b,
            text=url.replace(
                "https://", ""
            )
            .replace("http://", "")
            .replace(
                "blob://", ""
            )[:25],
        )
        note.select(
            note.index("end") - 1
        )
        b.NewWindow = (
            lambda url: makenew(
                url
            )
            or "break"
        )

    def exitFile():
        """
        从note中删除current标签对应的tab页

        Args:
            无

        Returns:
            无
        """
        index = note.index(
            "current"
        )
        selected_tab = note.tab(
            index
        )

        note.forget(index)

    def padpopout(event):
        """
        显示右键菜单

        Args:
            event: 触发鼠标事件的对象

        Returns:
            None
        """
        padPopOutMenu.post(
            event.x_root,
            event.y_root,
        )
        root.update()

    from tkinter import ttk

    root = tk.Tk()

    note = ttk.Notebook()

    note.pack(
        expand=1, fill="both"
    )
    makenew(
        "https://www.baidu.com"
    )

    padPopOutMenu = tk.Menu(root)

    padPopOutMenu.add_command(
        label="新建页面",
        command=makenew(
            "https://www.baidu.com"
        ),
    )

    padPopOutMenu.add_command(
        label="关闭页面",
        command=exitFile,
    )

    note.bind(
        "<Button-3>", padpopout
    )

    root.title("浏览器")
    root.geometry("800x600")

    maincefloop()

    root.mainloop()

    bye()
