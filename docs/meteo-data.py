# Example module used with the meteo service.

def getWeather(zip):
    return [
        {'zip': zip, 'date': '2008-06-07', 'type': 17, 'temparature': 18},
        {'zip': zip, 'date': '2008-06-08', 'type': 6, 'temparature': 21},
        {'zip': zip, 'date': '2008-06-09', 'type': 10, 'temparature': 21},
        {'zip': zip, 'date': '2008-06-10', 'type': 14, 'temparature': 20},
    ]
