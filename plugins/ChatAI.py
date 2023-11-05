import tkinter
import tkinter as tk
import urllib.request
import urllib.parse
import json


def ChatAI(myStr):
    """
    使用青云客免费版ChatAI接口实现聊天功能

    Args:
        myStr (str): 用户输入的聊天内容

    Returns:
        str: ChatAI返回的聊天内容
    """
    try:
        # 对输入的字符串进行url编码
        text = urllib.parse.quote(
            myStr
        )
        # 构造请求的URL
        url = "{}={}".format(
            "http://api.qingyunke.com/api.php?key=free&appid=0&msg",
            text,
        )
        # 打开URL并获取响应
        response = (
            urllib.request.urlopen(
                url
            )
        )
        # 将响应内容解码为utf-8编码
        responses = (
            response.read().decode(
                "utf-8"
            )
        )
        # 将解码后的内容解析为json格式
        responseText = json.loads(
            responses
        )
        # 返回json中指定的字段内容
        return responseText[
            "content"
        ]
    except:
        # 发生异常时返回错误信息
        return "错误"


class ChatInterface:
    def __init__(self, master):
        """
        初始化函数，创建一个包含聊天窗口和消息输入框的聊天窗口类

        Args:
            master: 聊天窗口的主窗口

        Returns:
            None
        """
        # 创建一个Frame对象，master为它的主窗口
        self.frame = tkinter.Frame(
            master
        )

        # 在主窗口中打包Frame对象，填充整个窗口
        self.frame.pack(
            fill="both"
        )

        # 创建一个Text对象，用于显示聊天窗口的内容
        self.chat_window = tk.Text(
            self.frame,
            bd=1,
            bg="white",
            height="8",
            width="50",
            font=("Arial", 12),
        )
        # 设置聊天窗口的状态为禁用，防止用户编辑内容
        self.chat_window.config(
            state=tk.DISABLED
        )

        # 创建一个Scrollbar对象，命令为聊天窗口的yview，即滚动条的动作
        self.scrollbar = tk.Scrollbar(
            self.frame,
            command=self.chat_window.yview,
            cursor="heart",
        )
        # 设置聊天窗口的yscrollcommand为scrollbar的set方法，实现滚动条的效果
        self.chat_window[
            "yscrollcommand"
        ] = self.scrollbar.set

        # 创建一个Entry对象，用于用户输入消息
        self.message_entry = (
            tk.Entry(
                self.frame,
                bd=1,
                bg="white",
                font=("Arial", 12),
            )
        )
        # 当用户按下回车键时，调用send_message方法发送消息
        self.message_entry.bind(
            "<Return>",
            self.send_message,
        )

        # 创建一个Button对象，用于发送消息
        self.send_button = tk.Button(
            self.frame,
            text="Send",
            font=("Arial", 12),
            width="10",
            height=5,
            bd=0,
            bg="#32de97",
            activebackground="#3c9d9b",
            fg="#ffffff",
            command=self.send_message,
        )

        # 将滚动条放置在（x=476, y=6, height=386）的位置
        self.scrollbar.place(
            x=476, y=6, height=386
        )
        # 将聊天窗口放置在（x=6, y=6, height=386, width=470）的位置
        self.chat_window.place(
            x=6,
            y=6,
            height=386,
            width=470,
        )
        # 将消息输入框放置在（x=6, y=401, height=40, width=370）的位置
        self.message_entry.place(
            x=6,
            y=401,
            height=40,
            width=370,
        )
        # 将发送按钮放置在（x=384, y=401, height=40）的位置
        self.send_button.place(
            x=384, y=401, height=40
        )

    def send_message(self):
        """
        发送消息并显示在聊天窗口中。

        Args:
            无参数。

        Returns:
            无返回值。

        """
        # 获取输入框中的消息
        message = (
            self.message_entry.get()
        )
        # 清空输入框中的内容
        self.message_entry.delete(
            0, tk.END
        )
        # 如果消息不为空
        if message != "":
            # 将聊天窗口配置为正常状态
            self.chat_window.config(
                state=tk.NORMAL
            )
            # 在聊天窗口中插入消息
            self.chat_window.insert(
                tk.END,
                "You: "
                + message
                + "\n\n",
            )
            # 调用ChatAI函数并插入返回的消息到聊天窗口
            self.chat_window.insert(
                tk.END,
                "ChatAI:"
                + ChatAI(message)
                + "\n\n",
            )
            # 将聊天窗口配置为禁用状态，不能进行编辑操作
            self.chat_window.config(
                state=tk.DISABLED
            )
            # 滚动到聊天窗口的最后一条消息
            self.chat_window.yview(
                tk.END
            )
