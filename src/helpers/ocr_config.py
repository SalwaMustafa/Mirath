OCR_CONFIG = {
    
    "headers": lambda token: {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    },
    "payload": lambda file_base64: {
        "file": file_base64,
        "fileType": 1,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False
    }
}
