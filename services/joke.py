from __future__ import annotations

import sqlite3
from pathlib import Path

def _get_data_path() -> Path:
    """
    回傳 data/jokes.db 的路徑（相對於這個 jokes.py 檔案的位置）。
    這樣你不管從哪個工作目錄執行，都找得到 jokes.db。
    """
    base_dir = Path(__file__).resolve().parent.parent  # bot/
    return base_dir / 'data' / 'jokes.db'

def _get_connection():    #只負責
    db_path = _get_data_path()
    con = sqlite3.connect(db_path)
    return con
    
def pick_one_joke(category: str | None = None) -> str:
    con = _get_connection()
    cursor = con.cursor()
    
    cursor.execute("""SELECT content
    FROM jokes
    WHERE category ='冷笑話'
    ORDER BY RANDOM()
    LIMIT 1;""")
    row = cursor.fetchone()

    con.close()
    if row is None:
        return "笑話資料庫目前沒有資料"
    return row[0]
    
if __name__ == "__main__":
    # 允許你直接 python services/jokes.py 自測
    print(pick_one_joke())


'''
if category:
# 有分類
    cursor.execute(sql_with_where, (category,))
else:
# 沒分類
    cursor.execute(sql_all)
'''