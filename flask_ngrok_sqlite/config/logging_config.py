import datetime
from logging import DEBUG, INFO
from pathlib import Path

"""
ログ設計指針
https://qiita.com/nanasess/items/350e59b29cceb2f122b3

◆バッチ処理の例◆
INFO 処理開始時
INFO 途中経過
INFO 処理終了時
WARN イベント発生時
ERROR 例外発生時
INFO その他、必要に応じて

◆WEBアプリケーションの例◆
INFO リクエスト開始時 - 処理概要、実行クラス名、メソッド名
INFO 途中経過 - 実行条件、処理対象オブジェクトのキーとなる値等(customer_id, order_id 等)
INFO 処理終了時 - 実行結果(OK/NG 等)、リダイレクト先
WARN イベント発生時 - 画面に表示したエラーメッセージ等
ERROR 例外発生時 - 例外クラス、例外メッセージ
INFO その他、必要に応じて
"""
"""    ★ Python　ログレベルについて　★
DEBUG   10  問題探求に必要な詳細な情報を出力したい場合
INFO    20  想定内の処理が行われた場合
WARNING 30  想定外の処理やそれが起こりそうな場合
ERROR   40  重大な問題により、機能を実行出来ない場合
CRITICAL    50  プログラムが実行不可となるような重大なエラーが発生した場合
"""

# ファイル名に入れる日付フォーマット
today = datetime.datetime.now().strftime("%Y-%m-%d")

ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT_DIR / f"log/{today}"

if LOG_DIR.exists() is False:
    LOG_DIR.mkdir()


# class LoggingConf():
LOGGING_CONFIG = {
    "version": 1,
    # ログフォーマット設定
    "formatters": {
        "info": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
        'error': {
            "format": "%(asctime)s %(levelname)s %(name)s %(process)d "
            "%(message)s",
        }
    },
    # ハンドラー設定
    "handlers": {
        # 標準出力ハンドラー
        "debug_console_handler": {
            "level": DEBUG,
            "formatter": "info",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        # ファイル出力ハンドラー
        # log file のサイズがmaxBytesを超えると、info1, 2, 3..nと
        # 新しいlog fileを作成(rotating)し、backCountで指定した数だけ
        "info_rotating_file_handler": {
            "level": INFO,
            "formatter": "info",
            "class": "logging.handlers.RotatingFileHandler",
            # ログファイルを出力したい場所のパスとファイル名を指定
            "filename": LOG_DIR / "info.log",
            "mode": "a",
            "maxBytes": 1048576,  # 1MB
            "backupCount": 10,
            "encoding": "utf-8",
        },
        "error_file_handler": {
            "level": INFO,
            # "level": ERROR,
            "formatter": "error",
            "class": "logging.FileHandler",
            # ログファイルを出力したい場所のパスとファイル名を指定
            "filename": LOG_DIR / "error.log",
            "mode": "a",
            "encoding": "utf-8",
        }
    },
    # ロガー設定
    "loggers": {
        "": {
            "handlers": [
                "debug_console_handler",
                "info_rotating_file_handler",
                "error_file_handler",
            ],
            "level": "NOTSET",
            "propagate": 0
        }
    }
}
