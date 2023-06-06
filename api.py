from flask import Flask, request, jsonify
import requests
import datetime
from config import open_weather_token
import json


app = Flask(__name__)

    
@app.route('/weather', methods =['GET'])


def get_weather_api():

    city = request.args.get('city')

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")

        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        if cur_weather < -20:
            temperature_advice = "It's unbelievably cold. You need thermal underwear, a warm sweatshirt and jacket. Wool socks would be nice."
        elif cur_weather < -15:
            temperature_advice = "Very cold. I need thermal underwear, a warm sweater, and a jacket."
        elif cur_weather < -10:
            temperature_advice = "It's pretty cold. You need a warm coat and jacket."
        elif cur_weather < -5:
            temperature_advice = "It's cold. Wear a warm jacket."
        elif cur_weather < 0:
            temperature_advice = "It's chilly. A warm jacket is enough"
        elif cur_weather < 5:
            temperature_advice = "It's chilly. A warm jacket is enough"
        elif cur_weather < 10:
            temperature_advice = "It's chilly. Wear a light jacket."
        elif cur_weather < 15:
            temperature_advice = "It's not cold. Wear a sweatshirt."
        elif cur_weather < 20:
            temperature_advice = "It's warm. You can go in a T-shirt, but take a sweatshirt."
        elif cur_weather < 25:
            temperature_advice = "It's very warm. You can wear a t-shirt or shirt."
        elif cur_weather < 30:
            temperature_advice = "It's hot. Put on a T-shirt and get a bottle of water"
        elif cur_weather < 35:
            temperature_advice = "It's very hot. Put on a T-shirt and a cap and get a bottle of water."
        elif cur_weather < 40:
            temperature_advice = "It's unbelievably hot. It's better to sit at home under the air conditioning.)"
        else:
            temperature_advice = "Where are you?!"


        return jsonify({
            "temperature": cur_weather,
            "feels_like": feels_like,
            "temperature_advice": temperature_advice,
        })

    except Exception as ex:
        return jsonify({
            "errror": str(ex)
        })
    
@app.route('/stime', methods =['GET'])
def get_stime_api():

    city = request.args.get('city')

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")

        data = r.json()

        city = data["name"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        return jsonify({
            "sunrise_time": sunrise_time,
            "sunset_time": sunset_time
        })

    except Exception as ex:
        return jsonify({
            "errror": str(ex)
        })

@app.route('/wd', methods =['GET'])
def get_wd_api():

    city = request.args.get('city')

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")

        data = r.json()

        city = data["name"]
        wind = data["wind"]["speed"]
        weather_description = data["weather"][0]["main"]

        if weather_description == "light rain":
            weather_advice = "It's light rain. An umbrella comes in handy."
        elif weather_description == "moderate rain":
            weather_advice = "It's moderate rain. An umbrella comes in handy."
        elif weather_description == "heavy intensity rain":
            weather_advice = "It's heavy intensity rain. An umbrella comes in handy."
        elif weather_description == "very heavy rain":
            weather_advice = "It's very heavy rain. An umbrella comes in handy."
        elif weather_description == "extreme rain":
            weather_advice = "It's extreme rain. An umbrella comes in handy."
        elif weather_description == "freezing rain":
            weather_advice = "It's freezing rain. An umbrella comes in handy."
        elif weather_description == "light intensity shower rain":
            weather_advice = "It's light intensity shower rain. An umbrella comes in handy."
        elif weather_description == "shower rain":
            weather_advice = "It's shower rain. An umbrella comes in handy."
        elif weather_description == "heavy intensity shower rain":
            weather_advice = "It's heavy intensity shower rain. An umbrella comes in handy."
        elif weather_description == "ragged shower rain":
            weather_advice = "It's ragged shower rain. An umbrella comes in handy."
        elif weather_description == "thunderstorm with light rain":
            weather_advice = "It's thunderstorm with light rain. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm with rain":
            weather_advice = "It's thunderstorm with rain. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm with heavy rain":
            weather_advice = "It's thunderstorm with heavy rain. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "light thunderstorm":
            weather_advice = "It's light thunderstorm. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm":
            weather_advice = "It's thunderstorm. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "heavy thunderstorm":
            weather_advice = "It's heavy thunderstorm. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "ragged thunderstorm":
            weather_advice = "It's ragged thunderstorm. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm with light drizzle":
            weather_advice = "It's thunderstorm with light drizzle. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm with drizzle":
            weather_advice = "It's thunderstorm with drizzle. An umbrella would come in handy. But I'd stay home.)"
        elif weather_description == "thunderstorm with heavy drizzle":
            weather_advice = "It's thunderstorm with heavy drizzle. An umbrella would come in handy. But I'd stay home.)"
        else:
            weather_advice = "It's not raining. An umbrella is not useful."

        return jsonify({
            "wd": weather_description,
            "wind": wind,
            "weather_advice": weather_advice,
        })

    except Exception as ex:
        return jsonify({
            "errror": str(ex)
        })
    
@app.route('/forecast', methods=['GET'])
def get_forecast_api():
    city = request.args.get('city')

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric")
        data = r.json()

        forecast_data = []
        city_name = data["city"]["name"]
        for i in data['list']:
                
            if i['main']['temp'] < -20:
                temperature_advice = "It's unbelievably cold. You need thermal underwear, a warm sweatshirt and jacket. Wool socks would be nice."
            elif i['main']['temp'] < -15:
                temperature_advice = "Very cold. I need thermal underwear, a warm sweater, and a jacket."
            elif i['main']['temp'] < -10:
                temperature_advice = "It's pretty cold. You need a warm coat and jacket."
            elif i['main']['temp'] < -5:
                temperature_advice = "It's cold. Wear a warm jacket."
            elif i['main']['temp'] < 0:
                temperature_advice = "It's chilly. A warm jacket is enough"
            elif i['main']['temp'] < 5:
                temperature_advice = "It's chilly. A warm jacket is enough"
            elif i['main']['temp'] < 10:
                temperature_advice = "It's chilly. Wear a light jacket."
            elif i['main']['temp'] < 15:
                temperature_advice = "It's not cold. Wear a sweatshirt."
            elif i['main']['temp'] < 20:
                temperature_advice = "It's warm. You can go in a T-shirt, but take a sweatshirt."
            elif i['main']['temp'] < 25:
                temperature_advice = "It's very warm. You can wear a t-shirt or shirt."
            elif i['main']['temp'] < 30:
                temperature_advice = "It's hot. Put on a T-shirt and get a bottle of water"
            elif i['main']['temp'] < 35:
                temperature_advice = "It's very hot. Put on a T-shirt and a cap and get a bottle of water."
            elif i['main']['temp'] < 40:
                temperature_advice = "It's unbelievably hot. It's better to sit at home under the air conditioning.)"
            else:
                temperature_advice = "Where are you?!"

            if i['weather'][0]['description'] == "light rain":
                weather_advice = "It's light rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "moderate rain":
                weather_advice = "It's moderate rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "heavy intensity rain":
                weather_advice = "It's heavy intensity rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "very heavy rain":
                weather_advice = "It's very heavy rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "extreme rain":
                weather_advice = "It's extreme rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "freezing rain":
                weather_advice = "It's freezing rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "light intensity shower rain":
                weather_advice = "It's light intensity shower rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "shower rain":
                weather_advice = "It's shower rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "heavy intensity shower rain":
                weather_advice = "It's heavy intensity shower rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "ragged shower rain":
                weather_advice = "It's ragged shower rain. An umbrella comes in handy."
            elif i['weather'][0]['description'] == "thunderstorm with light rain":
                weather_advice = "It's thunderstorm with light rain. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm with rain":
                weather_advice = "It's thunderstorm with rain. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm with heavy rain":
                weather_advice = "It's thunderstorm with heavy rain. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "light thunderstorm":
                weather_advice = "It's light thunderstorm. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm":
                weather_advice = "It's thunderstorm. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "heavy thunderstorm":
                weather_advice = "It's heavy thunderstorm. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "ragged thunderstorm":
                weather_advice = "It's ragged thunderstorm. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm with light drizzle":
                weather_advice = "It's thunderstorm with light drizzle. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm with drizzle":
                weather_advice = "It's thunderstorm with drizzle. An umbrella would come in handy. But I'd stay home.)"
            elif i['weather'][0]['description'] == "thunderstorm with heavy drizzle":
                weather_advice = "It's thunderstorm with heavy drizzle. An umbrella would come in handy. But I'd stay home.)"
            else:
                weather_advice = "It's not raining. An umbrella is not useful."

            forecast_entry = {
                'date': i['dt_txt'],
                'temperature': i['main']['temp'],
                'description': i['weather'][0]['description'],
                'temperature_advice': temperature_advice,
                'weather_advice': weather_advice,
            }
            forecast_data.append(forecast_entry)

        return jsonify({
            'city': city_name,
            'forecast': forecast_data
        })

    except Exception as ex:
        return jsonify({
            "error": str(ex)
        })



if __name__ == '__main__':
    app.run(port=5001)