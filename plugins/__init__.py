from .calculator import calculator
from .Calendar import MyCalendar
from .Regextool import RegexTest
from .ChatAI import ChatInterface
from .Browser import test


pluginMarket = "PyEditor"

plugins = [
    (
        "计算器",
        "一个简单易用的计算器",
        "0.07",
        calculator,
    ),
    (
        "日历",
        "一个简单易用的日历",
        "0.11",
        MyCalendar,
    ),
    (
        "正则表达式工具",
        "一个正则表达式工具",
        "0.06",
        RegexTest,
    ),
    (
        "聊天AI",
        "一个有趣的闲聊AI",
        "0.01",
        ChatInterface,
    ),
    (
        "浏览器",
        "一个内置的简易浏览器",
        "0.03",
        False,
        test,
    ),
]
