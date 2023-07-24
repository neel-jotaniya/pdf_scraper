import requests
import json
API_URL = "https://api-inference.huggingface.co/models/neel-jotaniya/distilbert-base-uncased-finetuned-emotion"
headers = {"Authorization": "Bearer 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"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query("i am very angry and sad")
print(data)