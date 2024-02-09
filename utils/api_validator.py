def check_api_success(response_json: dict) -> bool:
    """
    Check if the API response is successful
    """
    return response_json["success"] is True
