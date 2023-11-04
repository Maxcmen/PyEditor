import ttkbootstrap as ttk
import re

from ttkbootstrap.dialogs import (
    Messagebox,
)


class RegexTest:
    def __init__(self, master):
        """
        初始化函数

        Args:
            master: 创建界面的窗口对象

        Returns:
            None
        """
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
            """
            匹配文本框中符合正则表达式规则的内容，并将结果输出到匹配框中。

            Args:
                无参数。

            Returns:
                无返回值。

            """
            try:
                # 编译正则表达式
                Regex = re.compile(
                    self.regex_text.get()
                )
                # 在文本框中查找所有匹配的内容
                match_text = re.findall(
                    Regex,
                    self.text_box.get(
                        "1.0",
                        "end",
                    ),
                )

                # 清空匹配框
                self.match_box.delete(
                    "1.0", "end"
                )

                # 将匹配结果插入到匹配框中
                self.match_box.insert(
                    "end",
                    match_text,
                )

            except Exception as e:
                # 发生异常时，显示错误信息对话框
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
