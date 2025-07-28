import json
import re
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def generate_blood_report_summary(blood_data):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": (
                        "You are a clinical hematologist AI assistant." 
                        "Analyze the full CBC report provided. "
                        "For each parameter (WBC, RBC, Hemoglobin, Platelets, etc.)," 
                        "state whether it is within normal range or abnormal. If abnormal," 
                        "explain the possible cause. If normal, simply say it is normal." 
                        "Provide a complete breakdown of all parameters in a professional and reassuring tone."

            )
        },
        {
            "role": "user",
            "content": f"### CBC Report:\n{blood_data}"
        }
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.4
    )
    raw_reply = response.choices[0].message.content
    reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
    return reply

if __name__ == "__main__":
    with open("biological_data_flat.json", "r") as file:
        blood_data = json.load(file)
    print(generate_blood_report_summary(blood_data))
