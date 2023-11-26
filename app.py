from flask import Flask, request,jsonify
import requests
import json
import asyncio

def webhook(event,url):
    method = event.method
    urlFrom = event.url
    print(f"headersType:{type(event.headers)}")
    headers = {key: value for key, value in dict(event.headers).items() if key != 'Host'} 
    body = event.json

    print(f"Method: {method}\nType:{type(method)}")
    print(f"URL_FROM: {urlFrom}\nType:{type(url)}")
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
    
    body = request.json
    msg = body["events"][0]["message"]["text"]
    if msg.startswith("あまおとくん"):
        serviceURL = [
            'https://gpt-bot.userlocal.jp/bot/e8449bb8',
            'https://script.google.com/macros/s/AKfycby-2Fmm9VymDqU5cEnzadScSkmCoosUKlxhcTgPD9KjNliMpiNA8cfLQO-ZLOrzP0MOxQ/exec'
        ]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [webhook(request, url) for url in serviceURL]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
        print("All tasks completed:", results)
    
    return "complete", 200
        

if __name__ == '__main__':
    app.run(port=3000)
