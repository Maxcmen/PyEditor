import ttkbootstrap as ttk

from .setting import (
    saveConfig,
    settings,
)


class SettingPad:
    def __init__(self, master):
        """
        Editor设置初始化函数

        Args:
            master: 顶层容器

        Returns:
            None

        """
        self.frame = ttk.Frame(
            master
        )

        self.setting = settings

        self.styleSetting = (
            ttk.Labelframe(
                self.frame
            )
        )
        self.styleSetting.pack(
            side="top",
            fill="x",
            padx=15,
            pady=20,
        )

        self.styleSettingLabel = (
            ttk.Label(
                self.styleSetting,
                text="编辑器风格: ",
            )
        )

        self.styleSettingLabel.pack(
            side="left", padx=10
        )

        styles = (
            ttk.Style().theme_names()
        )

        self.styleSettingCombobox = ttk.Combobox(
            self.styleSetting,
            values=styles,
            state="readonly",
        )

        self.styleSettingCombobox.pack(
            side="right", padx=10
        )

        self.styleSettingCombobox.bind(
            "<<ComboboxSelected>>",
            self.styleSettingCombobox_select,
        )

        self.alphaSetting = (
            ttk.Labelframe(
                self.frame
            )
        )
        self.alphaSetting.pack(
            side="top",
            fill="x",
            padx=15,
            pady=20,
        )

        self.alphaSettingLabel = (
            ttk.Label(
                self.alphaSetting,
                text="编辑器透明度: ",
            )
        )

        self.alphaSettingLabel.pack(
            side="left", padx=10
        )

        self.alphaSettingScale = ttk.Scale(
            self.alphaSetting,
            from_=0,
            to=100,
            length=500,
            command=self.alpahSettingScale_change,
        )

        self.alphaSettingScale.pack(
            side="right",
            padx=10,
        )

        self.fontSetting = (
            ttk.Labelframe(
                self.frame
            )
        )
        self.fontSetting.pack(
            side="top",
            fill="x",
            padx=15,
            pady=20,
        )

        self.fontSettingLabel = (
            ttk.Label(
                self.fontSetting,
                text="编辑器字体: ",
            )
        )
        self.fontSettingLabel.pack(
            side="left", padx=10
        )

        self.fontSettingCombobox = ttk.Combobox(
            self.fontSetting,
            values=[
                "黑体",
                "宋体",
                "微软雅黑",
            ],
        )

        self.fontSettingCombobox.pack(
            side="right", padx=10
        )

        self.fontSettingCombobox.bind(
            "<<ComboboxSelected>>",
            self.fontSettingCombobox_select,
        )

        self.fontsizeSetting = (
            ttk.Labelframe(
                self.frame
            )
        )
        self.fontsizeSetting.pack(
            side="top",
            fill="x",
            padx=15,
            pady=20,
        )

        self.fontsizeSettingLabel = ttk.Label(
            self.fontsizeSetting,
            text="编辑器字体大小: ",
        )

        self.fontsizeSettingLabel.pack(
            side="left", padx=10
        )

        self.fontSettingSpinner = ttk.Spinbox(
            self.fontsizeSetting,
            values=[
                str(i)
                for i in range(
                    1, 20
                )
            ],
            command=self.fontsizeSettingSpinner_change,
        )

        self.fontSettingSpinner.pack(
            side="right", padx=10
        )

        self.encodeSetting = (
            ttk.Labelframe(
                self.frame
            )
        )
        self.encodeSetting.pack(
            side="top",
            fill="x",
            padx=15,
            pady=20,
        )

        self.encodeSettingLabel = (
            ttk.Label(
                self.encodeSetting,
                text="编辑器编码: ",
            )
        )
        self.encodeSettingLabel.pack(
            side="left", padx=10
        )

        self.encodeSettingCombobox = ttk.Combobox(
            self.encodeSetting,
            values=[
                "utf-8",
                "gbk",
            ],
        )

        self.encodeSettingCombobox.pack(
            side="right", padx=10
        )

        self.encodeSettingCombobox.bind(
            "<<ComboboxSelected>>",
            self.encodeSettingCombobox_select,
        )

        self.saveSetting = ttk.Button(
            self.frame,
            text="保存设置",
            command=self.saveSetting_click,
        )
        self.saveSetting.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20,
        )

    def saveSetting_click(self):
        """
        保存设置并点击保存按钮时的函数。

        Args:
            无参数。

        Returns:
            无返回值。

        """
        saveConfig(self.setting)

    def encodeSettingCombobox_select(
        self, event
    ):
        """
        将编码方式设置到设置字典中的函数

        Args:
        - event: 事件对象，可选参数，此函数不使用该参数

        Returns:
        - None: 该函数没有返回值
        """
        encode = (
            self.encodeSettingCombobox.get()
        )
        self.setting[
            "encode"
        ] = encode

    def fontsizeSettingSpinner_change(
        self,
    ):
        """
        当字体大小调节器(Spinner)的值发生变化时，更新设置中心中的字体大小值。

        Args:
            无参数。

        Returns:
            无返回值。

        """
        fontsize = (
            self.fontSettingSpinner.get()
        )
        self.setting[
            "fontsize"
        ] = fontsize

    def fontSettingCombobox_select(
        self, event
    ):
        """
        事件处理函数，设置字体下拉框选择事件的处理函数

        Args:
            event: 事件对象，当前选择事件触发时传入的参数

        Returns:
            None

        """
        font = (
            self.fontSettingCombobox.get()
        )
        self.setting["font"] = font

    def alpahSettingScale_change(
        self, event
    ):
        """
        Alpha滑块值改变事件处理函数

        Args:
            event: 事件对象，与事件类型相关

        Returns:
            None

        """
        alpha = (
            self.alphaSettingScale.get()
        )
        alpha = int(alpha) / 100
        self.setting[
            "alpha"
        ] = str(alpha)

    def styleSettingCombobox_select(
        self, event
    ):
        """
        函数功能：设置样式下拉框选择时的回调函数，更新设置字典中的样式值

        Args:
            event: combobox 事件对象，可选参数，此函数不使用该参数

        Returns:
            None
        """
        style = (
            self.styleSettingCombobox.get()
        )
        self.setting[
            "style"
        ] = style
