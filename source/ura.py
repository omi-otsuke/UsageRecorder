from collections.abc import Iterable
import datetime
import os
import sys
import tomllib
import wx.adv
import urlog
import vld
import ur
import ure

# TODO(Low): 項目を表す変数名をできるだけ統一させる。
# TODO(Mid): 複数人で使用した時、利用者ごとにモード判別ができるようにする。


class UsageRecorderApp(wx.App):
    def OnInit(self):
        system_conf_file_path = os.path.join(
            os.path.dirname(__file__), "../conf/system_conf.toml"
        )
        with open(system_conf_file_path, "rb") as f:
            self.system_conf = tomllib.load(f)
        wx.Log.SetActiveTarget(urlog.LogFile(self.system_conf["log_file_path"]))
        # NOTE: LogXXXインスタンスを属性で保持することによって、segmentation faultの
        # 発生を防止している。
        self.log_message_box = urlog.LogMessageBox()
        self.log_chain = wx.LogChain(self.log_message_box)
        frame = InputFrame()
        frame.Show()
        return True


class InputFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, wx.ID_ANY, "サーバー使用履歴記録ツール", size=(500, 400)
        )

        system_conf_file_path = os.path.join(
            os.path.dirname(__file__), "../conf/system_conf.toml"
        )
        with open(system_conf_file_path, "rb") as f:
            self.system_conf = tomllib.load(f)

        # 最上位のパネル
        root_panel = wx.Panel(self, wx.ID_ANY)

        # root_panelの下に子パネルを置く。
        self.record_mode_panel = RecordModePanel(root_panel)
        self.datetime_data_panel = DatetimePanel(root_panel)
        self.user_panel = UserPanel(root_panel)
        self.purpose_panel = PurposePanel(root_panel)
        self.destination_panel = DestinationPanel(root_panel)
        self.remarks_panel = RemarksPanel(root_panel)
        self.decision_button_panel = DecisionButtonPanel(root_panel)

        # パネルの配置を調整する。
        root_layout = wx.BoxSizer(wx.VERTICAL)
        root_layout.Add(
            self.record_mode_panel,
            0,
            wx.EXPAND | wx.TOP | wx.BOTTOM,
            border=10,
        )
        root_layout.Add(
            self.datetime_data_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border=10
        )
        root_layout.Add(self.user_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)
        root_layout.Add(
            self.purpose_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border=10
        )
        root_layout.Add(
            self.destination_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border=10
        )
        root_layout.Add(
            self.remarks_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border=10
        )
        root_layout.Add(
            self.decision_button_panel,
            0,
            wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM,
            border=10,
        )
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)
        self.Fit()

        try:
            self.usage_recorder = ur.UsageRecorder()
        except FileNotFoundError as e:
            wx.LogError(str(e))
            sys.exit("FileNotFoundError")
        except OSError as e:
            wx.LogError(str(e))
            sys.exit("OSError")
        self.recording_state = self.usage_recorder.check_state()

        # Excelのデータ入力状況に応じて記録モードを決定する。
        if self.recording_state == ur.RecordingState.WAITING_FOR_INPUT_BEGIN_TIME:
            self.record_mode_panel.begin_radiobutton.SetValue(True)
            self.change_begin_mode_display()
        elif self.recording_state == ur.RecordingState.WAITING_FOR_INPUT_END_TIME:
            self.record_mode_panel.end_radiobutton.SetValue(True)
            self.change_end_mode_display()
        else:
            # 異常状態の場合、エラーメッセージを表示してアプリを終了する。
            wx.MessageBox(
                "出力先Excelファイルが意図しない内容になっています。"
                + os.linesep
                + "Excelファイルを修正してから再度本アプリを起動してください。",
                "出力先Excelファイルの異常",
                wx.ICON_ERROR,
            )
            self.Destroy()
        self.record_mode_panel.begin_radiobutton.Disable()
        self.record_mode_panel.end_radiobutton.Disable()

        # イベントとメソッドを紐づける。
        self.Bind(
            wx.EVT_BUTTON,
            self.on_ok_button_pressed,
            self.decision_button_panel.ok_button,
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_close_button_pressed,
            self.decision_button_panel.close_button,
        )

    def change_begin_mode_display(self):
        # ユーザーデータを読み込んで画面に表示する。
        self.user_data = self.usage_recorder.load_user_data()
        self.user_panel.user_name_text.SetValue(self.user_data["user_name"])
        self.user_panel.account_name_text.SetValue(self.user_data["connection_account"])
        self.purpose_panel.purpose_combobox.SetValue(self.user_data["use_purpose"])
        for checkbox in self.destination_panel.destination_checkboxes:
            checkbox.SetValue(False)
        for checkbox in self.destination_panel.destination_checkboxes:
            for server_name in self.user_data["server_names"]:
                if checkbox.GetLabel() == server_name:
                    checkbox.SetValue(True)
        self.remarks_panel.remarks_text.SetValue(self.user_data["remarks"])

        self.datetime_data_panel.end_date_picker.Disable()
        self.datetime_data_panel.end_time_picker.Disable()

    def change_end_mode_display(self):
        # Excelのデータを読み込んで画面に表示する。
        entity = self.usage_recorder.read_data()
        self.datetime_data_panel.begin_date_picker.SetValue(entity.begin_datetime)
        self.datetime_data_panel.begin_time_picker.SetValue(entity.begin_datetime)
        self.user_panel.user_name_text.SetValue(entity.user_name)
        self.user_panel.account_name_text.SetValue(entity.connection_account)
        self.purpose_panel.purpose_combobox.SetValue(entity.use_purpose)
        for checkbox in self.destination_panel.destination_checkboxes:
            checkbox.SetValue(False)
        for checkbox in self.destination_panel.destination_checkboxes:
            for server_name in entity.server_names:
                if checkbox.GetLabel() == server_name:
                    checkbox.SetValue(True)
        self.remarks_panel.remarks_text.SetValue(entity.remarks)

    def set_background_colour_all(self, field, colour):
        """指定されたフィールドの背景色を変更する。"""
        if isinstance(field, Iterable):
            for i in field:
                i.SetBackgroundColour(colour)
                i.Refresh()
        else:
            field.SetBackgroundColour(colour)
            field.Refresh()

    def on_ok_button_pressed(self, event):
        """アプリに入力された値を取得しUsageRecorderに渡す。
        その後別プログラムを呼び出して本アプリを閉じる。
        """
        entity = ure.UsageRecordEntity()
        begin_date = self.datetime_data_panel.begin_date_picker.GetValue()
        begin_time = self.datetime_data_panel.begin_time_picker.GetValue()
        entity.begin_datetime = datetime.datetime(
            begin_date.GetYear(),
            begin_date.GetMonth() + 1,
            begin_date.GetDay(),
            begin_time.GetHour(),
            begin_time.GetMinute(),
            begin_time.GetSecond(),
        )
        end_date = self.datetime_data_panel.end_date_picker.GetValue()
        end_time = self.datetime_data_panel.end_time_picker.GetValue()
        entity.end_datetime = datetime.datetime(
            end_date.GetYear(),
            end_date.GetMonth() + 1,
            end_date.GetDay(),
            end_time.GetHour(),
            end_time.GetMinute(),
            end_time.GetSecond(),
        )
        entity.user_name = self.user_panel.user_name_text.GetValue()
        entity.connection_account = self.user_panel.account_name_text.GetValue()
        entity.use_purpose = self.purpose_panel.purpose_combobox.GetValue()
        entity.server_names = []
        for checkbox in self.destination_panel.destination_checkboxes:
            if checkbox.IsChecked():
                entity.server_names.append(checkbox.GetLabel())
        entity.remarks = self.remarks_panel.remarks_text.GetValue()
        entity.update_date = datetime.date.today()

        # バリデーション対象をリストに格納する。
        self.fields = []
        self.fields.append(self.user_panel.user_name_text)
        self.fields.append(self.user_panel.account_name_text)
        self.fields.append(self.purpose_panel.purpose_combobox)
        self.fields.append(self.destination_panel.destination_checkboxes)

        # バリデーションの結果にエラーがあった場合、メッセージを表示して入力待ち状態に戻る。
        invalid_fields = []
        for field in self.fields:
            if isinstance(field, Iterable):
                # NOTE: イテラブルなオブジェクトは各グループの0番目からバリデーターを取れば良い。
                validator = field[0].GetValidator()
            else:
                validator = field.GetValidator()
            if validator.Validate(self):
                self.set_background_colour_all(
                    field, wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
                )
            else:
                invalid_fields.append(validator.label_name.rstrip(" *"))
                self.set_background_colour_all(field, "pink")

        if len(invalid_fields) > 0:
            bullet = os.linesep + "・"
            wx.MessageBox(
                "下記項目の入力内容に誤りがあります。"
                + bullet
                + bullet.join(invalid_fields),
                "入力エラー",
                wx.OK | wx.ICON_ERROR,
            )
            return

        usage_recorder = ur.UsageRecorder()
        usage_recorder.check_state()
        usage_recorder.load_user_data()
        if self.record_mode_panel.begin_radiobutton.GetValue():
            # 開始状態の時、Excelへの書き込みが完了したらRDPを呼び出す。
            self.recording_state = ur.RecordingState.WAITING_FOR_INPUT_BEGIN_TIME
            usage_recorder.write_data(self.recording_state, entity)
            os.execv(self.system_conf["application"], self.system_conf["arguments"])
        else:
            # 終了状態の時、Excelへの書き込みが完了したらアプリを終了する。
            self.recording_state = ur.RecordingState.WAITING_FOR_INPUT_END_TIME
            usage_recorder.write_data(self.recording_state, entity)
            self.Destroy()

    def on_close_button_pressed(self, event):
        self.Destroy()


class RecordModePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        record_mode_label = wx.StaticText(
            self, wx.ID_ANY, "記録モード", size=(90, wx.DefaultSize.y)
        )
        self.begin_radiobutton = wx.RadioButton(self, wx.ID_ANY, "開始")
        self.end_radiobutton = wx.RadioButton(self, wx.ID_ANY, "終了")

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(
            record_mode_label,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=10,
        )
        child_layout = wx.GridSizer(cols=2, gap=(0, 0))
        child_layout.Add(
            self.begin_radiobutton, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=50
        )
        child_layout.Add(
            self.end_radiobutton, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, border=50
        )
        layout.Add(child_layout, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


class DatetimePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        # TODO(Low): 現在時刻を反映させるボタンを設置する。
        begin_datetime_label = wx.StaticText(
            self, wx.ID_ANY, "使用開始日時 *", size=(90, wx.DefaultSize.y)
        )
        self.begin_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        self.begin_time_picker = wx.adv.TimePickerCtrl(self, wx.ID_ANY)
        end_datetime_label = wx.StaticText(
            self, wx.ID_ANY, "使用終了日時 *", size=(90, wx.DefaultSize.y)
        )
        self.end_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        self.end_time_picker = wx.adv.TimePickerCtrl(self, wx.ID_ANY)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(
            begin_datetime_label,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=10,
        )
        layout.Add(self.begin_date_picker, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(self.begin_time_picker, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(
            end_datetime_label,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=10,
        )
        layout.Add(self.end_date_picker, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(self.end_time_picker, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


class UserPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        user_name_label = wx.StaticText(
            self, wx.ID_ANY, "利用者 *", size=(90, wx.DefaultSize.y)
        )
        self.user_name_text = wx.TextCtrl(
            self,
            wx.ID_ANY,
            size=(200, wx.DefaultSize.y),
            validator=vld.ValueExistsValidator(user_name_label.GetLabel()),
        )
        account_name_label = wx.StaticText(
            self, wx.ID_ANY, "接続アカウント *", size=(90, wx.DefaultSize.y)
        )
        self.account_name_text = wx.TextCtrl(
            self,
            wx.ID_ANY,
            size=(200, wx.DefaultSize.y),
            validator=vld.ValueExistsValidator(account_name_label.GetLabel()),
        )

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(
            user_name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, border=10
        )
        layout.Add(self.user_name_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(
            account_name_label,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=10,
        )
        layout.Add(self.account_name_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


class PurposePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        system_conf_file_path = os.path.join(
            os.path.dirname(__file__), "../conf/system_conf.toml"
        )
        with open(system_conf_file_path, "rb") as f:
            self.system_conf = tomllib.load(f)

        purpose_label = wx.StaticText(
            self, wx.ID_ANY, "使用目的 *", size=(90, wx.DefaultSize.y)
        )
        self.purpose_choices = self.system_conf["purpose_choices"]
        self.purpose_combobox = wx.ComboBox(
            self,
            wx.ID_ANY,
            "選択または自由記述して下さい。",
            size=(200, wx.DefaultSize.y),
            choices=self.purpose_choices,
            validator=vld.ValueExistsValidator(purpose_label.GetLabel()),
        )

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(
            purpose_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, border=10
        )
        layout.Add(
            self.purpose_combobox,
            1,
            wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE | wx.LEFT | wx.RIGHT,
            border=10,
        )
        self.SetSizer(layout)


class DestinationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        system_conf_file_path = os.path.join(
            os.path.dirname(__file__), "../conf/system_conf.toml"
        )
        with open(system_conf_file_path, "rb") as f:
            self.system_conf = tomllib.load(f)

        destination_label = wx.StaticText(
            self, wx.ID_ANY, "接続先サーバー *", size=(90, wx.DefaultSize.y)
        )
        self.destination_names = self.system_conf["destination_names"]
        self.destination_checkboxes = []
        for destination_name in self.destination_names:
            self.destination_checkboxes.append(
                wx.CheckBox(
                    self,
                    wx.ID_ANY,
                    destination_name,
                )
            )
        self.destination_checkboxes[0].SetValidator(
            vld.AtLeastOneValidator(
                self.destination_checkboxes, destination_label.GetLabel()
            )
        )

        # TODO(Mid): サーバーのグループ毎に枠を作る。
        # TODO(Mid): 縦方向に並べる。
        layout = wx.BoxSizer(wx.HORIZONTAL)
        child_layout = wx.GridSizer(cols=2, gap=(0, 0))
        layout.Add(
            destination_label,
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=10,
        )
        for checkbox in self.destination_checkboxes:
            child_layout.Add(checkbox, 0, wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, border=5)
        layout.Add(child_layout, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


class RemarksPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        remarks_label = wx.StaticText(
            self, wx.ID_ANY, "備考", size=(90, wx.DefaultSize.y)
        )
        self.remarks_text = wx.TextCtrl(self, wx.ID_ANY, size=(200, wx.DefaultSize.y))

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(
            remarks_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, border=10
        )
        layout.Add(self.remarks_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


class DecisionButtonPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.ok_button = wx.Button(self, wx.ID_OK)
        self.close_button = wx.Button(self, wx.ID_CLOSE)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        buttons_layout = wx.StdDialogButtonSizer()
        buttons_layout.AddButton(self.ok_button)
        buttons_layout.AddButton(self.close_button)
        buttons_layout.Realize()
        layout.Add(buttons_layout, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.SetSizer(layout)


if __name__ == "__main__":
    app = UsageRecorderApp()
    app.MainLoop()
