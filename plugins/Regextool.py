import ttkbootstrap as ttk
import re

from ttkbootstrap.dialogs import (
    Messagebox,
)


class RegexTest:
    def __init__(self, master):
        self.frame = ttk.Frame(
            master
        )

        self.frame.pack(
            fill="both",
            expand=True,
        )

        self.regex_text = (
            ttk.Entry(
                self.frame,
                width=50,
            )
        )
        self.regex_text.pack(
            side="top",
            fill="x",
            anchor="n",
            padx=25,
            pady=50,
        )

        self.text_box = ttk.Text(
            self.frame, height=15
        )

        self.text_box.pack(
            side="top", fill="x"
        )

        def match_text():
            try:
                Regex = re.compile(
                    self.regex_text.get()
                )
                match_text = re.findall(
                    Regex,
                    self.text_box.get(
                        "1.0",
                        "end",
                    ),
                )

                self.match_box.delete(
                    "1.0", "end"
                )

                self.match_box.insert(
                    "end",
                    match_text,
                )

            except Exception as e:
                Messagebox(
                    title="错误",
                    message=e,
                )

        self.match_button = (
            ttk.Button(
                self.frame,
                text="匹配",
                command=match_text,
            )
        )

        self.match_button.pack(
            side="top",
            fill="x",
            pady=20,
            padx=500,
        )

        self.match_box = ttk.Text(
            self.frame, height=15
        )

        self.match_box.pack(
            side="top", fill="x"
        )
