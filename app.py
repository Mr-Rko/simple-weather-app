from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Shared HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Poppins", sans-serif;
        }
        body {
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        input {
            width: 80%;
            padding: 10px;
            border: 2px solid #66a6ff;
            border-radius: 10px;
            margin-bottom: 15px;
            outline: none;
            text-align: center;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #66a6ff;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #5594e6;
        }
        .weather {
            margin-top: 20px;
            font-size: 1.1em;
        }
        .temp {
            font-size: 2em;
            font-weight: bold;
            margin-top: 10px;
            color: #0077b6;
        }
        .footer {
            margin-top: 20px;
            font-size: 0.85em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Simple Weather App</h1>
        <form method="POST" action="/weather">
            <input type="text" name="city" placeholder="Enter city name" required>
            <br>
            <button type="submit">Get Weather</button>
        </form>
        {% if weather %}
        <div class="weather">
            <p><strong>{{ weather['city'] }}</strong></p>
            <p class="temp">{{ weather['temp'] }}°C</p>
            <p>{{ weather['desc'] }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def hello_world():
    return render_template_string(html_template)

@app.route('/health')
def health():
    return 'Server is up and running'

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = "44228539048b3a7ec2834e06ec662d66"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            weather_data = {"city": city, "temp": "N/A", "desc": "City not found!"}
        else:
            weather_data = {
                "city": data['name'],
                "temp": data['main']['temp'],
                "desc": data['weather'][0]['description'].title()
            }
    except Exception:
        weather_data = {"city": city, "temp": "N/A", "desc": "Error fetching data"}

    # Render page again with weather data
    return render_template_string(html_template, weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
