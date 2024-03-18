from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city):
    api_key = "xxxxxxxxxxxxxx" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    #showing all the retrieved information
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather(city)
        if weather_data["cod"] == 200:
            # Extracting relevant weather information
            weather_description = weather_data["weather"][0]["description"]
            temperature_kelvin = weather_data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            return render_template("weather.html", city=city, description=weather_description,
                                   temperature=temperature_celsius, humidity=humidity, wind_speed=wind_speed)
        else:
            error_message = f"Error: {weather_data['message']}"
            return render_template("error.html", error_message=error_message)
    #rendering the form to submit
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
