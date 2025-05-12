
def ok_response(data: dict):
    return {
        "status": "ok",
        "data": data
    }
    
def error_response(message: str):
    return {
        "status": "error",
        "message": message
    }