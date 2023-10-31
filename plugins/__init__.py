from .calculator import calculator
from .Calendar import MyCalendar
from .Browser import test
from .Regextool import RegexTest

pluginMarket = "PyEditor"

plugins = [
    (
        "计算器",
        "一个简单易用的计算器",
        "0.03",
        calculator,
    ),
    (
        "日历",
        "一个简单易用的日历",
        "0.04",
        MyCalendar,
    ),
    (
        "浏览器",
        "一个内置的简易浏览器",
        "0.03",
        False,
        test,
    ),
    (
        "正则表达式工具",
        "一个正则表达式工具",
        "0.01",
        RegexTest,
    ),
]
