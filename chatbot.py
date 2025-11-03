import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_response(user_input):
    if "HR" in user_input or "policy" in user_input.lower():
        return "You can refer to HR portal or contact HR department at hr@organization.com."
    elif "IT" in user_input.lower():
        return "For IT issues, please email support@organization.com."
    else:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Answer this question simply: {user_input}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
