import requests
from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
client.create_database('example')


def get_data_from_api():
    url = "https://api.frankfurter.app/2005-01-01..?from=USD&to=TRY"
    response = requests.request("GET", url)
    data = response.json()['rates']
    return data


def insert(data):
    json_body = []

    # index        => 0
    # key          => 2005-01-03
    # value['TRY'] => 1.3726
    for index, (key, value) in enumerate(data.items()):
        date_time_str = str(key)
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

        point = {
            "measurement": "USDTRY",
            "tags": {
                "id": index,
            },
            "time": date_time_obj,
            "fields": {
                "TRY": float(value['TRY']),
            }
        }
        json_body.append(point)
    result = (client.write_points(json_body))

    if (result):
        print("Success")
    else:
        print("Error")

    return result


def select():
    res = client.query("SELECT TRY FROM USDTRY")
    selected_data = list(res.get_points(measurement='USDTRY'))
    for item in selected_data:
        print(str(item['time']) +" "+ "TRY : "+str(item['TRY']))

    return selected_data
    
response_data = get_data_from_api()

db_ressult = insert(response_data)

print(db_ressult)

select()
