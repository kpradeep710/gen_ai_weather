from openai import OpenAI
import requests
import json
import os

NVDIA_TOKEN = os.getenv("nvdia_token")
OPENWEATHER_API_KEY = os.getenv("weather_api_key")
def get_current_weather_info(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# print(get_current_weather_info("New York"))
def get_temperature(city_name):
    url =f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def get_humidity(city_name):
    url =f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def ask_weather_assistant(prompt):
    client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
    )
    response = client.chat.completions.create(
        model="thinkingmachines/inkling",
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are a weather assistant. Your only job is to provide weather information "
                    "for the city mentioned in the user's prompt. "
                    "If the prompt does not ask about weather, or does not mention a city, "
                    "respond only with: \"I don't have information on that. I can only help with weather-related queries.\" "
                    "Do not answer questions unrelated to weather, even if you know the answer."
                )
            },
            {"role": "user", "content": prompt}
        ],
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'get_current_weather_info',
                    'description': 'Get current weather info for a given city',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'city': {
                                'type': 'string'
                            }
                        },
                        'required': ['city']
                    }
                }
            },

            {
                "type": "function",
                "function": {
                    "name": "get_temperature",
                    "description": "Get temperature for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string"
                            }
                        },
                        'required': ["city"]
                    }
                }
            },

            {
                "type": "function",
                "function": {
                    "name": "get_humidity",
                    "description": "Get humidity for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }   
        ],
        tool_choice='auto'
    )
    
    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

# AI requested a tool
    tool_call = message.tool_calls[0]

# Get the function name
    function_name = tool_call.function.name

# Get the function arguments
    args = json.loads(tool_call.function.arguments)

# Get city
    city = args["city"]


# Decide which Python function to execute
    if function_name == "get_current_weather_info":
        result = get_current_weather_info(city)

    elif function_name == "get_temperature":
        result = get_temperature(city)

    elif function_name == "get_humidity":
        result = get_humidity(city)
    else:
        return "Unknown function requested."

    # result= get_current_weather_info(city)

    final_response = client.chat.completions.create(
        model="thinkingmachines/inkling",
        messages=[
            {"role": "user", "content": prompt},
        message,
            {
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': json.dumps(result)
            }
m  c        ],
    )

    return final_response.choices[0].message.content

# print(ask_weather_assistant("what is the weather in Narasayapalem?"))
# print(ask_weather_assistant("what is the weather of narasayapalem village near to bapatla"))
while True:
    prompt = input("Enter your prompt: ")
    if prompt.lower() == "exit":
        print("Program stopped.")
        break
    result = ask_weather_assistant(prompt)
    print("AI:", result)
