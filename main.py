import openai
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

import requests

import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    # Replace with the origin of your Next.js app
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# OPEN_API_KEY = os.getenv('OPEN_API_KEY')
OPEN_API_KEY = "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"


# @app.post("/api/process-prompt")
# async def process_prompt(prompt: dict):

#     f_prompt = prompt.get('prompt')

#     if not f_prompt:
#         raise HTTPException(
#             status_code=400, detail="Missing 'prompt' field in request payload")

#     return {"message": "Processed prompt successfully"}

# response = await requests.post(
#     "https://api.openai.com/v1/engines/davinci-codex/completions",
#     headers={
#         "Authorization": f"Bearer {OPEN_API_KEY}",
#         "Content-Type": "application/json",
#     },
#     json={
#         "prompt": prompt,
#         "max_tokens": 1000,
#         "model": "gpt-3.5-turbo"
#     }
# )

# # Check if the request to the OpenAI API was successful
# if response.status_code != 200:
#     raise HTTPException(
#         status_code=response.status_code,
#         detail="Error processing prompt"
#     )

# # Get the response from the OpenAI API
# openai_response = response.json()

# # Return the OpenAI response to the original requester
# return openai_response["choices"][0]["text"]


# @app.post("/api/process-prompt")
# async def process_prompt(prompt: dict):

#     response = await requests.post(
#         "https://api.openai.com/v1/engines/davinci-codex/completions",
#         headers={
#             "Authorization": f"Bearer {OPEN_API_KEY}",
#             "Content-Type": "application/json",
#         },
#         json={
#             "prompt": prompt,
#             "max_tokens": 1000,
#             "model": "gpt-3.5-turbo"
#         }
#     )

#     # Check if the request to the OpenAI API was successful
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=response.status_code,
#             detail="Error processing prompt"
#         )

#     # Get the response from the OpenAI API
#     openai_response = response.json()

#     # Extract the desired text from the OpenAI response
#     text = openai_response["choices"][0]["text"]

#     # Create a response dictionary
#     response_data = {
#         "text": text
#     }

#     # Return the response as a JSON object
#     return response_data


# @app.post("/api/process-prompt")
# async def process_prompt(prompt: dict):
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://api.openai.com/v1/engines/davinci-codex/completions",
#             headers={
#                 "Authorization": f"Bearer {OPEN_API_KEY}",
#                 "Content-Type": "application/json",
#             },
#             json={
#                 "prompt": "hello",
#                 "max_tokens": 1000,
#                 "model": "gpt-3.5-turbo"
#             }
#         )

#         # Check if the request to the OpenAI API was successful
#         if response.status_code != 200:
#             raise HTTPException(
#                 status_code=response.status_code,
#                 detail="Error processing prompt"
#             )

#         # Get the response from the OpenAI API
#         openai_response = response.json()

#         # Extract the desired text from the OpenAI response
#         text = openai_response["choices"][0]["text"]

#         # Create a response dictionary
#         response_data = {
#             "text": text
#         }

#         # Return the response as a JSON object
#         return response_data


@app.post("/api/process-prompt")
async def process_prompt(prompt: dict):
    openai.api_key = OPEN_API_KEY
    f_prompt = prompt['prompt']

    # Make a request to the OpenAI API
    response = openai.ChatCompletion.create(
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f_prompt},
        ]
    )

    # Check if the request to the OpenAI API was successful
    # if response['code'] != 200:
    #     raise HTTPException(
    #         status_code=response['code'],
    #         detail="Error processing prompt"
    #     )

    # Extract the desired text from the OpenAI response
    text = response["choices"][0]["message"]["content"]
    print(text)
    print(type(text))

    # Create a response dictionary
    response_data = json.dumps(text)

    # Return the response as a JSON object
    return response_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
