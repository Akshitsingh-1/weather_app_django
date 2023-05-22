import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=4e770f5f4ecb7bae28812958dfd38eb2'
    #city = 'London'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        #pass

    form = CityForm()

    cities = City.objects.all()

    weather_data= []

    for city in cities:
        r = requests.get(url.format(city)).json()
        #print(r.text)

        if 'main' in r and 'weather' in r:
            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)

        else:
            # Handle the case where the response does not have the expected structure
            context = {'weather_data': weather_data, 'form' : form}
            return render(request, 'weather/weather.html', context)
        

    print(weather_data)
    
    context = {'weather_data': weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)