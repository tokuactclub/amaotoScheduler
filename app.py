from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/",methods=['POST'])
def main():
    return


@app.route('/webhook', methods=['POST'])
def webhook():
    method = request.method
    url = request.url
    headers = {key: value for key, value in request.headers if key != 'Host'}
    body = request.json

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

        print('Forwarded Data:', response.json())
        print('HTTP Status Code:', response.status_code)

        return 'Data forwarded successfully', 200
    except Exception as e:
        print('Error:', e)
        return 'Failed to forward data', 500
    


if __name__ == '__main__':
    app.run(port=3000)
