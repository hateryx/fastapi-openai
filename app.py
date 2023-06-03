from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

OPEN_API_KEY = "XXXXXXXXXx"


@app.post("/api/process-prompt")
async def process_prompt(prompt):

    response = await requests.post(
        "https://api.openai.com/v1/engines/davinci-codex/completions",
        headers={
            "Authorization": f"Bearer {OPEN_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "max_tokens": 1000,
            "model": "gpt-3.5-turbo"
        }
    )

    # Check if the request to the OpenAI API was successful
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error processing prompt"
        )

    # Get the response from the OpenAI API
    openai_response = response.json()

    # Return the OpenAI response to the original requester
    return openai_response["choices"][0]["text"]


if __name__ == "__main__":
    app()
