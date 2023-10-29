from .calculator import calculator
from .Calendar import MyCalendar
from .Browser import test

pluginMarket = "PyEditor"

plugins = [
    (
        "计算器",
        "一个简单易用的计算器",
        "0.01",
        calculator,
    ),
    (
        "日历",
        "一个简单易用的日历",
        "0.01",
        MyCalendar,
    ),
    (
        "浏览器",
        "一个内置的简易浏览器",
        "0.01",
        False,
        test,
    ),
]
