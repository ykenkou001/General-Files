import sqlite3
from pathlib import Path
from typing import Union


def create_db(dbname: str) -> None:
    """DBとTABLEを作成する関数

    Args:
        dbname (str): データベースの名前、もしくは、パス(e.g: test.db)
    """
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS api_result (id TEXT PRIMARY KEY,' +
        'status TEXT, result TEXT, message TEXT, metadata TEXT)')
    con.commit()
    con.close()


def select_data(db_path: Union[str, Path]) -> None:
    """DB内のtableの内容を確認する関数

    Args:
        db_path (Union[str, Path]): dbのパス
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM result")
    for row in cur:
        print(str(row[0]) + "," + str(row[1]))
    con.close()


def get_tables(db_path: Union[str, Path]) -> None:
    """DB内のtableの中身を確認する関数

    Args:
        db_path (Union[str, Path]): _description_
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())
    # cur.execute("drop table if exists result")


def insert_data(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = 'INSERT INTO TEST (id, name) values (?,?)'
    data = [2, '{name: "test", value: [1, 2, 3]}']
    cur.execute(sql, data)
    con.commit()
    con.close()
