from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = cf * amount
    final_amount = round(final_amount, 2)

    response = {
        "fulfillmentText": f"{amount} {source_currency} is {final_amount:.2f} {target_currency}"
    }

    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = f"https://api.fastforex.io/convert?from={source}&to={target}&amount=1&api_key=b5184c26bf-f17f817c19-t7246p"

    response = requests.get(url)
    response = response.json()

    return response["result"][target]


if __name__ == '__main__':
    app.run(debug=True)
