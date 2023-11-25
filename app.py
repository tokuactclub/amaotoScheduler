from flask import Flask, request, jsonify
import requests
import json
app = Flask(__name__)

@app.route("/",methods=['POST'])
def main():
    body=request.json
    {'destination': 'Ud686a6755685ed53407a76dd183cc82f', 'events': [{'type': 'message', 'message': {'type': 'text', 'id': '483373867147460721', 'quoteToken': 'zpxht856GpsRq9hDkQQHe69DEQ1yxu2KVKjGEW5vs4u2_KOEOPzaaJz0pTMJ7qsNnl-97gVyimImzJrsMYcdvGe5EGMYXsRjVcNS4gSvqRuGxMyY4eedM3GZk5fV8SqfntScw6R-L4uFf-2Na6mQzQ', 'text': 'さ'}, 'webhookEventId': '01HG4354B8PBWJH9AQ74AQKCAC', 'deliveryContext': {'isRedelivery': False}, 'timestamp': 1700944580461, 'source': {'type': 'user', 'userId': 'Ue99cbbb0fb4a6cb510c2ea5f343f6715'}, 'replyToken': 'fb40266f492d4e2e8963926a593c1914', 'mode': 'active'}]}
    msg = body["events"][0]["message"]["text"]
@app.route('/webhook', methods=['POST'])
def webhook():
    method = request.method
    url = request.url
    headers = json.dumps({key: value for key, value in request.headers if key != 'Host'})
    body = json.dumps(request.json)

    print(f"Method: {method}\nType:{type(method)}")
    print(f"URL: {url}\nType:{type(url)}")
    print(f"Headers: {headers}\nType:{type(headers)}")
    print(f"Body: {body}\nType:{type(body)}")

    try:
        # Reconstruct headers and forward the request
        headers['Content-Type'] = 'application/json;charset=utf-8'
        response = requests.request(
            method=method,
            url='https://gpt-bot.userlocal.jp/bot/e8449bb8',
            headers=headers,
            json=body
        )
        print("end response")

        print('Forwarded Data:', response.json())
        print('HTTP Status Code:', response.status_code)

        return 'Data forwarded successfully', 200
    except Exception as e:
        print('Error:', e)
        return 'Failed to forward data', 500
    


if __name__ == '__main__':
    app.run(port=3000)
