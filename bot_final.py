from flask import Flask, request
import requests

app = Flask(__name__)

PHONE_ID = "Phone Number ID y Access Token"
TOKEN = "PEGAR_AQUI_TU_TOKEN"
VERIFY_TOKEN = "scania123"

DB = {
 "GRS905R": "SCANIA GRS905R 2008-2018 | R400 R440 | 2500Nm | 12+2 Opticruise+Retarder",
 "G33CM": "SCANIA G33CM 2022-Actual | >500HP | 3300Nm | 12+1 Nueva Gen Aluminio",
 "ATO3512F": "VOLVO ATO3512F FH16 750HP | 3550Nm | I-Shift Gen G",
 "16S221": "ZF 16S221 Actros MP3 MAN TGS | 2200Nm | 16 marchas Ecosplit",
 "RTLO16913A": "EATON RTLO16913A | 1650Nm | 13 marchas Roadranger",
 "G281-12": "MERCEDES G281-12 Powershift 3 Actros MP4 | 2800Nm | 12 marchas"
}

def enviar(to, texto):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"messaging_product":"whatsapp","to":to,"text":{"body":texto}}
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "error",403
    data = request.json
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' not in entry: return "ok",200
        msg = entry['messages'][0]['messages'][0]['text']['body'].upper()
        phone = entry['messages'][0]['messages'][0]['from']
        resp = DB.get(msg, f"No encontre {msg}. Prueba: GRS905R, G33CM, 16S221, RTLO16913A, G281-12")
        enviar(phone, resp)
    except: pass
    return "ok",200
