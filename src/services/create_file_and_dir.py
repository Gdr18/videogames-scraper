import json
import os
from datetime import datetime
from typing import Any

from src.enums.platform_enum import PlatformScrapperEnum

def select_or_create_path(path: str) -> str:
    path_src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(path_src, path)
    os.makedirs(directory, exist_ok=True)
    return directory

def create_and_write_file(data: Any, directory: str, filename: str) -> tuple:
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        if not isinstance(data, str):
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            f.write(data)
    return filepath, filename

def create_json_file(data: list[dict]) -> tuple:
    filename = f"videogames_{PlatformScrapperEnum(data[0]["platform"]).name.lower()}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.json"
    temp_dir = select_or_create_path("temp")
    
    return create_and_write_file(data, temp_dir, filename)
