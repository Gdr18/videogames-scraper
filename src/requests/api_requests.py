from flask import current_app

from src.enums.platform_enum import PlatformDBEnum
from src.requests.base_request import http_request


def login_api() -> str:
    login_url = current_app.config["API_LOGIN"]
    email = current_app.config["API_EMAIL"]
    password = current_app.config["API_PASSWORD"]

    url = f"{login_url}"
    payload = {"email": email, "password": password}
    response = http_request(url, "post", payload)

    if response.status_code != 200:
        raise Exception(f"Fallo en el login: {response.status_code} - {response.text}")

    return response.json().get("access_token", "")


def post_game_api(videogame: dict) -> bool:
    post_url = current_app.config["API_POST_GAME"]

    if not post_url:
        raise ValueError("La URL de la API no está configurada")

    # * Validación de plataformas aceptadas para el registro - Se puede modificar según necesidades
    valid_platforms = [platform.value for platform in PlatformDBEnum]
    if not videogame.get("platform") in valid_platforms:
        raise ValueError(f"Plataformas válidas para el registro: {valid_platforms}")

    token = current_app.config["TOKEN"]
    api_url = current_app.config["API_LOGIN"]

    if not token and api_url:
        token = login_api()
        if not token:
            raise Exception("No se pudo obtener el token de autenticación")

    url = f"{post_url}"

    response = http_request(url, "post", videogame, token)

    if response.status_code != 201:
        print(
            f"Fallo en el registro. Status code: {response.status_code}, Response: {response.text}"
        )
        return False
    print(f"Registro exitoso: {videogame.get('title')} ({videogame.get('platform')})")
    return True
