import os
import sys
import tomllib


def get_base_dir():
    """ベースディレクトリを取得する。"""
    if getattr(sys, "frozen", False):
        # .exe（PyInstallerでビルドされた実行ファイル）の場合
        return os.path.dirname(sys.executable)
    else:
        # .pyスクリプトとして実行された場合
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def get_system_conf_file_path():
    """システム設定ファイルのディレクトリを取得する。"""
    return os.path.join(get_base_dir(), "conf/system_conf.toml")


def get_user_data_file_path():
    """ユーザーデータファイルのパスを取得する。"""
    return os.path.join(get_base_dir(), "conf/user_data.toml")


def get_output_file_path():
    """出力ファイルのパスを取得する。"""
    with open(get_system_conf_file_path(), "rb") as f:
        system_conf = tomllib.load(f)
    return os.path.join(get_base_dir(), system_conf["output_file_path"])


def get_log_dir():
    """ログファイルのディレクトリを取得する。"""
    with open(get_system_conf_file_path(), "rb") as f:
        system_conf = tomllib.load(f)
    log_dir = os.path.join(get_base_dir(), system_conf["log_file_path"])
    return log_dir
