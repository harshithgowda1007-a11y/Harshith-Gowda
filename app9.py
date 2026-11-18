from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# 
API_KEY = "d78aa7854ff6922eda19344aee117b99"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q=Bengaluru&appid=d78aa7854ff6922eda19344aee117b99"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='Mysore')
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        # 1. Safely handle the response JSON object directly
        data = response.json()
        
        # 2. Check if OpenWeatherMap returned a success code (200) inside their JSON
        if response.status_code == 200:
            formatted = {
                "city": data.get("name"),
                "temperature": data["main"]["temp"],
                # 🟢 FIX: Added the [0] index accessor array tracker to pull the description correctly
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            return jsonify(formatted)
        else:
            # 🟢 FIX: Return OpenWeatherMap's actual error message instead of crashing the server
            return jsonify({
                "status": "Failed to fetch weather data",
                "api_error_code": data.get("cod"),
                "api_response_message": data.get("message", "Unknown API error occurred")
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "status": "Internal script handling error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)