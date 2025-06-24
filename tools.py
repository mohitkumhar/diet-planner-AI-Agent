from langchain.tools import Tool
import requests
import os

def fetch_calorie(foods: str):

    url = f"https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": os.environ["YOUR_APP_ID"],
        "x-app-key": os.environ["YOUR_APP_KEY"],
        "Content-Type": "application/json",
    }

    data = {
        "query": foods
    }

    response = requests.post(url, headers=headers, json=data)
    
    return response.json()

fetch_cal = Tool(
    name='featch_food_calorie',
    func=fetch_calorie,
    description="Featching Food Data",
)
