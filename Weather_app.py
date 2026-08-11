from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "5950a2aab802bc74cd29ccad1928b139"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return {
            "city": city.title(),
            "description": data["weather"][0]["description"].title(),
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"]
        }
    else:
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/weather")
def api_weather():
    city=request.args.get("city","London")
    weather_data = get_weather(city)

    if weather_data:
        return jsonify(weather_data)
    return jsonify({"error": "City not found"}), 404

from flask import send_from_directory

@app.route("/manifest.json")
def manifest():
    return send_from_directory("templates", "manifest.json")

@app.route("/sw.js")
def service_worker():
    return send_from_directory(".", "sw.js")

# def main():
#     print("=== Weather App ===")
#     print("Type 'exit' to quit\n")

#     while True:
#         city = input("Enter City name: ").strip()

#         if city.lower() == "exit":
#             break

    #    get_weather(city)


if __name__ == "__main__":
    app.run(debug=True, port=5000)