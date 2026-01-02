import json
import os
from datetime import datetime

from src.platform_enum import PlatformScrapperEnum


def create_json_file(data: list[dict]) -> tuple:
    filename = f"videogames_{PlatformScrapperEnum(data[0]["platform"]).name.lower()}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.json"
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
    filepath = os.path.join(temp_dir, filename)

    os.makedirs(temp_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return filepath, filename
