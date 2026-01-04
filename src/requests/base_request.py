from typing import Literal
import requests


def http_request(url: str, method: Literal["get", "post"] = "get", payload: dict = None,
	token: str = None) -> requests.Response:
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {token}" if token else None
	}
	
	if method == "post":
		return requests.post(url, json=payload, headers=headers)
	
	return requests.get(url)