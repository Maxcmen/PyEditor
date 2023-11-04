# PyEditor

**我们相信PyEditor是Python的未来.**

# 项目介绍

PyEditor是2023年10月2日由包括我在内的几位开发者发起的，
目前处于开发阶段。
但是目前PyEditor已经支持了一个编辑器的大部分功能。

PyEditor是有Python语言开发的，
GUI界面基于ttkbootstrap库开发的。

因此PyEditor相较与Python自动的IDLE更加的符合现代人的审美

虽然现在PyEditor并不是十分的稳定，而且有许多为完善的功能及未解决的bug。
但是PyEditor已经可以满足日常的编程需求，而且更新速度很快。

# 为什么选择我们

我们虽然现在并不是十分的稳定，但是我们依然建议初学者及大佬尝试我们的编辑器。

选择我们的编辑器有以下几个原因：
- PyEditor的配置十分简单，十分容易上手。
- 有基本的Python代码编辑功能，包括：高亮显示，代码补全
- Pyeditor内置很多有用的插件，还内置浏览器
- 界面十分美观，且支持主题切换，更加符合现代人的审美
- 目前更新速度十分的快，新的功能会不断加入
- 编辑器内置三种深色主题，两种浅色主题

# 环境配置

PyEditor使用Python3.9开发，因此建议使用Python3.9。

Pyeditor目前的运行方式是通过本地安装依赖来运行。

因此我们需要先拉取代码，然后安装依赖。

拉取PyEditor代码:
    git clone https://github.com/Maxcmen/PyEditor.git

PyEditor需要安装以下依赖：
- ttkbootstrap(>1.10)  GUI界面支持
- cefpython3(>66.1)    浏览器支持

安装命令需要使用pip安装：

    pip install ttkbootstrap 
    pip install cefpython3

请注意要安装后才可以正常使用PyEditor

# 目前的功能和未来规划

目前PyEditor的功能如下：
- 文件资源管理器
- 高亮显示
- 代码补全
- 多文件编辑切换
- 预览图片
- 插件

PyEditor的未来规划如下：

PyEditor v0.25:
- 重构、优化代码
- 修复一些bug
- 添加功能

PyEditor v0.30:
- 添加编辑器设置功能
- 完善插件功能
- 更加灵动的布局
- 完善代码高亮显示，代码补全功能

PyEdiotr v0.40:
- 添加语法检查
- 修复运行无法输入的功能
- 添加终端
- 添加插件市场
