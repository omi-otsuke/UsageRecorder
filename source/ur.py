import datetime
import os
from openpyxl import load_workbook
import tomllib
from enum import Enum
import urcmn
import ure


class UsageRecorder:
    def __init__(self):
        with open(urcmn.get_system_conf_file_path(), "rb") as f:
            self.system_conf = tomllib.load(f)
        self.output_file_path = urcmn.get_output_file_path()
        try:
            self.workbook = load_workbook(self.output_file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"指定されたファイルが見つかりません: {self.output_file_path}"
            ) from e
        except OSError as e:
            raise OSError(
                f"指定されたファイルが見つかりません: {self.output_file_path}"
                + os.linesep
                + "ファイルがネットワークフォルダにある場合、認証情報が正しくない可能性があります。"
            ) from e
        self.sheet = self.workbook[self.system_conf["sheet_name"]]
        self.BASE_ROW = self.system_conf["base_row"]

        self.row = self.BASE_ROW
        # 使用終了日時が空欄の行まで行数を加算する。
        while self.sheet["g" + str(self.row)].value is not None:
            self.row += 1

    def check_state(self):
        """使用開始、使用終了または異常のうちいずれの状態かを判断する。
        使用終了日時が空欄の行まで走査する方法で判断している。
        想定外のデータ入力がされていた場合、異常状態と判断する。
        """
        # 使用開始時刻が空欄の場合、開始時刻の入力待ち状態
        if self.sheet["f" + str(self.row)].value is None:
            # 入力必須セルか任意セルに値が入っている場合、異常状態
            if (
                self.sheet["b" + str(self.row)].value is not None
                or self.sheet["c" + str(self.row)].value is not None
                or self.sheet["d" + str(self.row)].value is not None
                or self.sheet["e" + str(self.row)].value is not None
                or self.sheet["h" + str(self.row)].value is not None
            ):
                return RecordingState.ABNORMAL_STATE
            return RecordingState.WAITING_FOR_INPUT_BEGIN_TIME
        # 使用開始時刻に値がある場合、終了時刻の入力待ち状態
        else:
            # 入力必須セルに値が入っていない場合、異常状態
            if (
                self.sheet["b" + str(self.row)].value is None
                or self.sheet["c" + str(self.row)].value is None
                or self.sheet["d" + str(self.row)].value is None
                or self.sheet["e" + str(self.row)].value is None
            ):
                return RecordingState.ABNORMAL_STATE
            return RecordingState.WAITING_FOR_INPUT_END_TIME

    def load_user_data(self):
        """ユーザーデータをファイルから読み込む。"""
        with open(urcmn.get_user_data_file_path(), "rb") as f:
            return tomllib.load(f)

    def read_data(self):
        """データをExcelから読み込む。"""
        # TODO(Low): 列の意味をシステム設定ファイルに定義する。
        return ure.UsageRecordEntity(
            datetime.datetime.strptime(
                self.sheet["f" + str(self.row)].value, "%Y/%m/%d %H:%M:%S"
            )
            if self.sheet["f" + str(self.row)].value is not None
            else datetime.datetime.now(),
            datetime.datetime.strptime(
                self.sheet["g" + str(self.row)].value, "%Y/%m/%d %H:%M:%S"
            )
            if self.sheet["g" + str(self.row)].value is not None
            else datetime.datetime.now(),
            self.sheet["b" + str(self.row)].value
            if self.sheet["b" + str(self.row)].value is not None
            else "",
            self.sheet["c" + str(self.row)].value
            if self.sheet["c" + str(self.row)].value is not None
            else "",
            self.sheet["d" + str(self.row)].value
            if self.sheet["d" + str(self.row)].value is not None
            else "",
            self.sheet["e" + str(self.row)].value.split(", ")
            if self.sheet["e" + str(self.row)].value is not None
            else [],
            self.sheet["h" + str(self.row)].value
            if self.sheet["h" + str(self.row)].value is not None
            else "",
            self.sheet["h1"].value
            if self.sheet["h1"].value is not None
            else datetime.date.today(),
        )

    def write_data(self, state, entity):
        """データをExcelに書き込む。"""
        # 次の入力セルを参照
        # TODO(Low): 列の意味をシステム設定ファイルに定義する。
        self.user_name = self.sheet["b" + str(self.row)]
        self.connection_account = self.sheet["c" + str(self.row)]
        self.use_purpose = self.sheet["d" + str(self.row)]
        self.server_names = self.sheet["e" + str(self.row)]
        self.begin_datetime = self.sheet["f" + str(self.row)]
        self.end_datetime = self.sheet["g" + str(self.row)]
        self.remarks = self.sheet["h" + str(self.row)]
        self.update_date = self.sheet["h1"]

        # 開始時刻の入力待ち状態の場合に更新する項目
        if state == RecordingState.WAITING_FOR_INPUT_BEGIN_TIME:
            self.end_datetime.value = None
        # 終了時刻の入力待ち状態の場合に更新する項目
        else:
            self.end_datetime.value = entity.end_datetime.strftime("%Y/%m/%d %H:%M:%S")

        # 状態に関わらず更新する項目
        self.user_name.value = entity.user_name
        self.connection_account.value = entity.connection_account
        self.use_purpose.value = entity.use_purpose
        self.server_names.value = ", ".join(entity.server_names)
        self.begin_datetime.value = entity.begin_datetime.strftime("%Y/%m/%d %H:%M:%S")
        self.remarks.value = entity.remarks
        self.update_date.value = entity.update_date

        self.workbook.save(self.output_file_path)


class RecordingState(Enum):
    """使用状態を定義する列挙型"""

    ABNORMAL_STATE = -1
    WAITING_FOR_INPUT_BEGIN_TIME = 0
    WAITING_FOR_INPUT_END_TIME = 1
