from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Young Dave Exchange</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #0f172a; color: white; padding: 20px; text-align: center; }
        h1 { color: #22c55e; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; margin: 20px auto; max-width: 400px; }
        input, select, button { padding: 12px; margin: 8px; border-radius: 8px; border: none; font-size: 16px; }
        button { background: #22c55e; color: black; font-weight: bold; width: 90%; }
        #result { font-size: 20px; margin-top: 15px; color: #fbbf24; }
    </style>
</head>
<body>
    <h1>🇳🇬 Young Dave Exchange</h1>
    <div class="card">
        <h3>Naira Calculator</h3>
        <input type="number" id="amount" placeholder="Enter Naira amount" value="1000">
        <br>
        <select id="currency">
            <option value="USD">US Dollar</option>
            <option value="EUR">Euro</option>
            <option value="GBP">British Pound</option>
            <option value="CAD">Canadian Dollar</option>
        </select>
        <br>
        <button onclick="convert()">Convert Now</button>
        <div id="result"></div>
    </div>
    <p>Built by Young Dave | Rates update live</p>

<script>
async function convert() {
    let amount = document.getElementById('amount').value;
    let currency = document.getElementById('currency').value;
    let res = await fetch(`/api/rate/${currency}?amount=${amount}`);
    let data = await res.json();
    if(data.error){
        document.getElementById('result').innerHTML = "Error: " + data.error;
    } else {
        document.getElementById('result').innerHTML = `${amount} NGN = <br><b>${data.converted} ${currency}</b>`;
    }
}
convert(); // Load rate on page open
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/rate/<currency>')
def get_rate(currency):
    try:
        amount = float(request.args.get('amount', 1))
        url = f"https://api.exchangerate-api.com/v4/latest/NGN"
        response = requests.get(url, timeout=10)
        data = response.json()
        rate = data['rates'].get(currency.upper())
        
        if rate:
            converted = round(rate * amount, 2)
            return jsonify({
                "from": "NGN",
                "to": currency.upper(),
                "rate": rate,
                "amount": amount,
                "converted": converted
            })
        else:
            return jsonify({"error": f"Currency {currency} not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
