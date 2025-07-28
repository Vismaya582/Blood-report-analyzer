import os
import requests
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

def fetch_nutrition_data(food_item):
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY
    }
    payload = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    response = requests.post(NUTRITIONIX_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json().get("foods", [])[0]
        return {
            "Calories": data.get("nf_calories"),
            "Protein": data.get("nf_protein"),
            "Fat": data.get("nf_total_fat"),
            "Carbs": data.get("nf_total_carbohydrate")
        }
    return {}

def generate_diet_plan(summary, metadata):
    try:
        age = metadata.get("age", "unknown")
        gender = metadata.get("gender", "unknown")

        food_sample = ["spinach", "eggs", "chicken", "oatmeal"]
        nutrition_info = ""
        for food in food_sample:
            info = fetch_nutrition_data(food)
            if info:
                nutrition_info += (
                    f"**{food}**: {info['Calories']} kcal, "
                    f"{info['Protein']}g protein, {info['Fat']}g fat, {info['Carbs']}g carbs\n"
                )

        user_prompt = (
            f"Patient Info:\n- Age: {age}\n- Gender: {gender}\n\n"
            f"Blood Report Summary:\n{summary}\n\n"
            f"Nutritional Info:\n{nutrition_info}\n\n"
            f"Please generate a medically sound, personalized diet plan. "
            f"Include:\n1. Summary\n2. Foods to include and avoid\n3. Example meal plan for a day\n4. Supplements if needed.\n"
            f"Use markdown formatting."
        )

        messages = [
            {
                "role": "system",
                "content": "You are a clinical dietitian. Generate diet plans based on CBC reports, patient metadata, and nutrition science."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )

        raw_reply = chat_completion.choices[0].message.content
        reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
        return reply

    except Exception as e:
        return f"❌ Error generating diet plan: {str(e)}"
