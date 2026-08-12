import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Make sure your OpenWeather API key is here
API_KEY = "5950a2aab802bc74cd29ccad1928b139"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/weather")
def get_weather():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    # 1. Fetch by precise location coordinates if available
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    # 2. Otherwise fetch by manual city name
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    else:
        # Fallback default if nothing is provided
        url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # Extract weather condition icon code (e.g. '10d' for rain, '01d' for clear sky)
        icon_code = data["weather"][0]["icon"] if "weather" in data else "02d"
        
        return jsonify({
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon_url": f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        })
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 400

if __name__ == "__main__":
    app.run(debug=True)