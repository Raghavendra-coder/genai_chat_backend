from together import Together
import os
from dotenv import load_dotenv
load_dotenv()
DEEPSEEK_API_KEY = os.environ.get("TOGETHER_API_KEY")
client = Together(api_key=DEEPSEEK_API_KEY)

def ai_model(question):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role":"user","content":f"{question}"}],
    )
    return response.choices[0].message.content


def file_process_ai(text, question):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "Answer the following question based on the given text:"},
            {"role": "user", "content": f"Text: {text}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content


def summarize_text(text):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "Summarize the following text:"},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content