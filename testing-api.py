import requests


API_KEY = ''

response = requests.get(
    f'https://calendarific.com/api/v2/holidays?api_key={API_KEY}&country={country}&year={year}')


print(response)
