from flask import current_app

from src.enums.platform_enum import PlatformDBEnum
from src.requests.base_request import http_request


def login_api() -> str:
	url = f"{current_app.config["API_URL"]}/auth/login"
	payload = {
		"email": current_app.config["API_EMAIL"],
		"password": current_app.config["API_PASSWORD"]
	}
	response = http_request(url, "post", payload)
	
	if response.status_code != 200:
		raise Exception(f"Fallo en el login: {response.status_code} - {response.text}")
	
	return response.json().get("access_token", "")


def post_game_api(videogame: dict) -> bool:
	valid_platforms = [platform.value for platform in PlatformDBEnum]
	if not videogame.get("platform") in valid_platforms:
		raise ValueError(f"Plataformas válidas para el registro: {valid_platforms}")
	
	token = login_api()
	
	if not token:
		raise Exception("No se pudo obtener el token de autenticación")
	
	url = f"{current_app.config["API_URL"]}/games/"

	response = http_request(url, "post", videogame, token)

	if response.status_code != 201:
		print(f"Fallo en el registro. Status code: {response.status_code}, Response: {response.text}")
		return False
	
	return True
	