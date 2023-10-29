import math
from ttkbootstrap import *


class calculator:
    def __init__(self, parent):
        def add_word(c):
            if c == "=":
                txt.replace(
                    "0.0",
                    "end",
                    eval(
                        txt.get(
                            "0.0",
                            "end",
                        )
                    ),
                )  # 填充计算结果
            else:
                txt.insert(
                    "end", c
                )  # 添加按钮输入内容

        def handler(fun, c):
            return lambda fun=fun, c=c: fun(
                c
            )

        self.frame = Frame(parent)
        self.frame.pack(
            anchor="center"
        )

        text_arr = [
            "1",
            "2",
            "3",
            "+",
            "4",
            "5",
            "6",
            "-",
            "7",
            "8",
            "9",
            "*",
            ".",
            "0",
            "=",
            "/",
        ]
        (
            ncol,
            bw,
            bh,
            padding,
            space,
            th,
        ) = (
            4,
            50,
            30,
            20,
            10,
            100,
        )  # 按钮列数、按钮宽度、高度、页面边距、按钮间边距、文本框高度
        nrow = math.ceil(
            len(text_arr)
            * 1.0
            / ncol
        )  # 按钮行数

        txt = Text(self.frame)
        txt.place(
            x=padding,
            y=padding,
            width=bw * ncol
            + space * (ncol - 1),
            height=th,
        )
        for index in range(
            len(text_arr)
        ):
            (
                row_index,
                col_index,
            ) = (index % ncol), (
                index // ncol
            )  # 行序号、列序号
            btn = Button(
                self.frame,
                text=text_arr[
                    index
                ],
                command=handler(
                    add_word,
                    text_arr[
                        index
                    ],
                ),
            )
            btn.place(
                x=padding
                + row_index
                * (bw + space),
                y=(
                    th
                    + padding * 2
                )
                + col_index
                * (bh + space),
                width=bw,
                height=bh,
            )
