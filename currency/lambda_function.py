import json
import requests

# Use your API key from Currency Layer
API_KEY = 'ba14c9ded0fb266e33212137c2129cad'
API_URL = 'http://api.currencylayer.com/live'

def lambda_handler(event, context):
    try:
        # Ensure that query parameters exist or provide default values
        base_currency = event.get('queryStringParameters', {}).get('base', 'USD')
        target_currency = event.get('queryStringParameters', {}).get('target', 'EUR')
        amount = event.get('queryStringParameters', {}).get('amount', 1)

        # Validate and convert amount to float
        try:
            amount = float(amount)
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid amount parameter"})
            }

        # Fetch exchange rates from Currency Layer API
        response = requests.get(f"{API_URL}?access_key={API_KEY}&currencies={target_currency}&source={base_currency}&format=1")
        data = response.json()

        # Check if the API request was successful
        if not data.get('success', False):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": data.get('error', {}).get('info', 'Failed to retrieve currency data')})
            }

        # Extract the exchange rate
        exchange_rate = data['quotes'].get(f'{base_currency}{target_currency}')
        if not exchange_rate:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Currency pair '{base_currency}-{target_currency}' not found"})
            }

        # Calculate the converted amount
        converted_amount = amount * exchange_rate

        # Return the result
        return {
            "statusCode": 200,
            "body": json.dumps({
                "base_currency": base_currency,
                "target_currency": target_currency,
                "exchange_rate": exchange_rate,
                "amount": amount,
                "converted_amount": converted_amount
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

