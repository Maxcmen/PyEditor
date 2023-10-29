from cefpython3 import (
    cefpython as cef,
)
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
            self.browser = browser

        def OnBeforePopup(
            self, target_url, **a
        ):
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
            self.browser_frame = (
                browser_frame
            )

        def OnSetFocus(
            self, source, **_
        ):
            return False

        def OnGotFocus(self, **_):
            """Fix CEF focus issues (#255). Call browser frame's focus_set
            to get rid of type cursor in url entry widget.
            """
            self.browser_frame.focus_set()

    def __init__(
        self, *a, url="", **b
    ):
        super().__init__(*a, **b)
        # create browser
        window_info = (
            cef.WindowInfo()
        )
        rect = [
            0,
            0,
            self.winfo_width(),
            self.winfo_height(),
        ]
        window_info.SetAsChild(
            self.get_window_handle(),
            rect,
        )
        if not url:
            url = "https://www.baidu.com/"
        self.browser = (
            cef.CreateBrowserSync(
                window_info,
                url=url,
            )
        )
        assert self.browser
        self.browser.SetClientHandler(
            self.LoadHandler(self)
        )
        self.browser.SetClientHandler(
            self.FocusHandler(self)
        )
        # fit frame
        self.bind(
            "<Configure>",
            self._configure,
        )

    def _configure(self, event):
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
        self.load(url)
        return "break"

    def loadurl(self, url):
        self.browser.StopLoad()
        self.browser.LoadUrl(url)

    def geturl(self):
        return (
            self.browser.GetUrl()
        )

    def reload(self):
        self.browser.Reload()

    def get_window_handle(self):
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
    cef.MessageLoopWork()
    tk._default_root.after(
        n, maincefloop, n
    )


def bye():
    cef.Shutdown()


def test():
    def makenew(url):
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

    from tkinter import ttk

    root = tk.Tk()
    note = ttk.Notebook()
    note.pack(
        expand=1, fill="both"
    )
    makenew("https://cn.bing.com/")
    root.title("浏览器")
    root.geometry("800x600")
    maincefloop()
    root.mainloop()
    bye()
