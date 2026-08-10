import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

NVIDIA_TOKEN = os.getenv("")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_TOKEN
)

response = client.chat.completions.create(
    model="thinkingmachines/inkling",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain about Python"}
    ]
)
# print(response)
print(response.choices[0].message.content)
