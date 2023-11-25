from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    method = request.method
    url = request.url
    headers = {key: value for key, value in request.headers if key != 'Host'}
    body = request.json

    print(f"Method: {method}")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Body: {body}")

    try:
        # Reconstruct headers and forward the request
        headers['Content-Type'] = 'application/json;charset=utf-8'
        response = requests.request(
            method=method,
            url='https://example.com/webhook',
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
