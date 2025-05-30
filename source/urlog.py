import datetime
import traceback
import wx


class LogFile(wx.Log):
    """ログをファイルに出力するためのログターゲット。"""

    def __init__(self, filepath):
        wx.Log.__init__(self)
        self.SetFormatter(LogFormatterForFile())
        self.filepath = filepath

    def DoLogText(self, message):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(message + traceback.format_exc())


class LogMessageBox(wx.Log):
    """ログをメッセージボックスに出力するためのログターゲット。"""

    def __init__(self):
        wx.Log.__init__(self)
        self.SetFormatter(LogFormatterForMessageBox())

    def DoLogText(self, message):
        wx.MessageBox(message, "エラー", wx.ICON_ERROR)


class LogFormatterForFile(wx.LogFormatter):
    def Format(self, level, message, info):
        timestamp = datetime.datetime.fromtimestamp(info.timestamp)
        return f"{timestamp:%Y-%m-%d %H:%M:%S} - "


class LogFormatterForMessageBox(wx.LogFormatter):
    def Format(self, level, message, info):
        return f"{message}"
