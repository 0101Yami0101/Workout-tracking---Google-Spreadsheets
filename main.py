#Workout tracking using google sheets
import requests
from datetime import datetime

APP_ID = "670f6f84"
API_KEY = "722fea07ab24c2bcfcee7e05328dc8ab"
ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise" #nutritionix


#User inputs 
query = input("Enter Query: ")

parameters = {
    "query": query,
    "gender": "male",
    "weight_kg": 60,
    "height_cm": 160,
    "age": 60
}

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}
response = requests.post(url=ENDPOINT, json= parameters, headers=header)
result =response.json()

#sheety transfer
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
SHEETY_ENDPOINT = "https://api.sheety.co/92a672567d3cfc17f5efb0cdc4a1a5c3/workoutTracking/workouts"
AUTH_KEY = "Basic eWFtaTpxd2VydHl1aW9wMTIzNDU2Nzg5MA"

header = {
    "Authorization": AUTH_KEY
}

#Creating nested list to input in Sheety API
for exercise in result["exercises"]:
    #sheety takes data in nested list format/nested property becomes "workout" as my project/sheet name/endpoint is "workouts"
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

sheet_response = requests.post(url = SHEETY_ENDPOINT, json = sheet_inputs, headers= header)
print(sheet_response.status_code)

#Optional: can change the authentication tokens and passwords as environment variables