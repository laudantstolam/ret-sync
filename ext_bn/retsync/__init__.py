#!/usr/bin/env python3

"""
Copyright (C) 2020, Alexandre Gazet.

This file is part of ret-sync plugin for Binary Ninja.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from collections import namedtuple

import binaryninjaui
if 'qt_major_version' in binaryninjaui.__dict__ and binaryninjaui.qt_major_version == 6:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QKeySequence
else:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QKeySequence

from binaryninjaui import UIAction, UIActionHandler
from binaryninja.plugin import PluginCommand

from .sync import SyncPlugin
from .retsync.rsconfig import rs_log


def add_commands(plugin):
    # Menu items under Plugins > ret-sync
    PluginCommand.register("ret-sync\\Enable Sync (Alt+S)",
        "Start ret-sync listener and accept debugger connection",
        lambda bv: plugin.cmd_sync())
    PluginCommand.register("ret-sync\\Disable Sync (Alt+Shift+S)",
        "Stop ret-sync listener",
        lambda bv: plugin.cmd_syncoff())
    PluginCommand.register("ret-sync\\Go (Alt+F5)",
        "Send go/continue to debugger",
        lambda bv: plugin.cmd_go())
    PluginCommand.register("ret-sync\\Step Over (F10)",
        "Send step-over to debugger",
        lambda bv: plugin.cmd_so())
    PluginCommand.register("ret-sync\\Step Into (F11)",
        "Send step-into to debugger",
        lambda bv: plugin.cmd_si())
    PluginCommand.register("ret-sync\\Set Breakpoint (F2)",
        "Set breakpoint at current cursor in debugger",
        lambda bv: plugin.cmd_bp())
    PluginCommand.register("ret-sync\\Set HW Breakpoint (Ctrl+F2)",
        "Set hardware breakpoint at current cursor",
        lambda bv: plugin.cmd_hwbp())
    PluginCommand.register("ret-sync\\Set One-shot Breakpoint (Alt+F3)",
        "Set one-shot breakpoint at current cursor",
        lambda bv: plugin.cmd_bp1())
    PluginCommand.register("ret-sync\\Translate Address (Alt+F2)",
        "Translate current cursor address for debugger",
        lambda bv: plugin.cmd_translate())

    # Hotkey bindings
    DbgAction = namedtuple('DbgAction', 'name, key_seq, handler')
    plugin_actions = (
        DbgAction("ret-sync\\Enable Sync (Alt+S)", QKeySequence(Qt.ALT | Qt.Key_S), UIAction(lambda ctx: plugin.cmd_sync())),
        DbgAction("ret-sync\\Disable Sync (Alt+Shift+S)", QKeySequence(Qt.ALT | Qt.SHIFT | Qt.Key_S), UIAction(lambda ctx: plugin.cmd_syncoff())),
        DbgAction("ret-sync\\Go (Alt+F5)", QKeySequence(Qt.ALT | Qt.Key_F5), UIAction(lambda ctx: plugin.cmd_go())),
        DbgAction("ret-sync\\Step Over (F10)", QKeySequence(Qt.Key_F10), UIAction(lambda ctx: plugin.cmd_so())),
        DbgAction("ret-sync\\Step Into (F11)", QKeySequence(Qt.Key_F11), UIAction(lambda ctx: plugin.cmd_si())),
        DbgAction("ret-sync\\Set Breakpoint (F2)", QKeySequence(Qt.Key_F2), UIAction(lambda ctx: plugin.cmd_bp())),
        DbgAction("ret-sync\\Set HW Breakpoint (Ctrl+F2)", QKeySequence(Qt.CTRL | Qt.Key_F2), UIAction(lambda ctx: plugin.cmd_hwbp())),
        DbgAction("ret-sync\\Set One-shot Breakpoint (Alt+F3)", QKeySequence(Qt.ALT | Qt.Key_F3), UIAction(lambda ctx: plugin.cmd_bp1())),
        DbgAction("ret-sync\\Translate Address (Alt+F2)", QKeySequence(Qt.ALT | Qt.Key_F2), UIAction(lambda ctx: plugin.cmd_translate())),
    )

    for action in plugin_actions:
        UIAction.registerAction(action.name, action.key_seq)
        UIActionHandler.globalActions().bindAction(action.name, action.handler)

    rs_log('commands added')


retsync_plugin = SyncPlugin()
add_commands(retsync_plugin)
