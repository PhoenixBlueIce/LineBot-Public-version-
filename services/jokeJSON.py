from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


def _get_data_path() -> Path:
    """
    回傳 data/jokes.json 的路徑（相對於這個 jokes.py 檔案的位置）。
    這樣你不管從哪個工作目錄執行，都找得到 jokes.json。
    """
    base_dir = Path(__file__).resolve().parent.parent  # bot/
    return base_dir / "data" / "jokes.json"

def load_jokes(path: Path | None = None) -> list[Any]:
    """
    讀取 jokes.json，回傳 jokes 清單。
    兼容兩種格式：
      1) {"jokes": [ ... ]}
      2) [ ... ]  （如果你直接把最外層寫成陣列）
    """
    path = path or _get_data_path()

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 兼容：外層是 dict，笑話在 key "jokes"
    if isinstance(data, dict):
        jokes = data.get("jokes", [])
        if not isinstance(jokes, list):
            raise ValueError('jokes.json 格式錯誤：["jokes"] 必須是 list')
        return jokes

    # 兼容：外層就是 list
    if isinstance(data, list):
        return data

    raise ValueError("jokes.json 格式錯誤：外層必須是 dict 或 list")

def normalize_joke(joke: Any) -> str:
    """
    將笑話資料轉成要回傳給使用者的乾淨字串。
    兼容：
      - "純字串"
      - {"content": "..."} 或 {"text": "..."}
    """
    if isinstance(joke, str):
        return joke.strip()

    if isinstance(joke, dict):
        # 你可以依你 jokes.json 的欄位命名習慣調整
        for key in ("content", "text", "joke"):
            val = joke.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return "這則笑話格式怪怪的，但我還是想逗你笑😅"

    return "笑話庫資料格式不太對，請我主人修一下🙏"

def pick_one_joke(path: Path | None = None) -> str:
    """
    隨機抽一則笑話，回傳字串。
    """
    jokes = load_jokes(path)
    if not jokes:
        return "笑話庫是空的，我現在也笑不出來🥲"

    return normalize_joke(random.choice(jokes))

if __name__ == "__main__":
    # 允許你直接 python services/jokes.py 自測
    print(pick_one_joke())
