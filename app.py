from flask import Flask, request,jsonify
import requests
import json

def webhook(event,url):
    method = event.method
    url = event.url
    print(f"headersType:{type(event.headers)}")
    headers = {key: value for key, value in dict(event.headers).items() if key != 'Host'} 
    body = event.json

    print(f"Method: {method}\nType:{type(method)}")
    print(f"URL: {url}\nType:{type(url)}")
    print(f"Headers: {headers}\nType:{type(headers)}")
    print(f"Body: {body}\nType:{type(body)}")

    try:
        # Reconstruct headers and forward the request
        headers["Content-Type"] = "application/json;charset=utf-8"
        response = requests.request(
            method=method,
            url=url,
            headers=json.loads(json.dumps(headers)),
            json=json.loads(json.dumps(body)),
        )

        print('Forwarded Data:', response)
        print('HTTP Status Code:', response.status_code)

        return 'Data forwarded successfully', 200
    except Exception as e:
        print('Error:', e)
        return 'Failed to forward data', 500
    


app = Flask(__name__)

@app.route("/",methods=['POST'])
def main():
    body=request.json
    {'destination': 'Ud686a6755685ed53407a76dd183cc82f', 'events': [{'type': 'message', 'message': {'type': 'text', 'id': '483373867147460721', 'quoteToken': 'zpxht856GpsRq9hDkQQHe69DEQ1yxu2KVKjGEW5vs4u2_KOEOPzaaJz0pTMJ7qsNnl-97gVyimImzJrsMYcdvGe5EGMYXsRjVcNS4gSvqRuGxMyY4eedM3GZk5fV8SqfntScw6R-L4uFf-2Na6mQzQ', 'text': 'さ'}, 'webhookEventId': '01HG4354B8PBWJH9AQ74AQKCAC', 'deliveryContext': {'isRedelivery': False}, 'timestamp': 1700944580461, 'source': {'type': 'user', 'userId': 'Ue99cbbb0fb4a6cb510c2ea5f343f6715'}, 'replyToken': 'fb40266f492d4e2e8963926a593c1914', 'mode': 'active'}]}
    msg : str = body["events"][0]["message"]["text"]
    if msg.startswith("あまおとくん"):
        serviceURL = ['https://gpt-bot.userlocal.jp/bot/e8449bb8','https://script.google.com/macros/s/AKfycby-2Fmm9VymDqU5cEnzadScSkmCoosUKlxhcTgPD9KjNliMpiNA8cfLQO-ZLOrzP0MOxQ/exec']
        for url in serviceURL:
            print(f"START ACCESS TO {url}")
            response = webhook(request,url)
            print(f"END ACCESS TO {url}\nRESPONSE:{response}")
    
    return "complete" ,200
        

if __name__ == '__main__':
    app.run(port=3000)
