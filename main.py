from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import openai

import os
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.getenv('OPENAI_API_KEY')
GATE_KEY = os.getenv('GATE_KEY')

app = FastAPI()

# for testing purposes
app.add_middleware(
    CORSMiddleware,
    # Replace with the origin of your Next.js app
    allow_origins=["https://next-ai-psych.vercel.app",
                   "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()


class User(BaseModel):
    username: str


def get_current_user(authorization: str = Header(...)):
    # Implement token verification logic here
    # You can decode and verify the token, retrieve the user information,
    # and check if the user has the required roles/permissions

    scheme, token = authorization.split(" ")

    if scheme.lower() != "bearer" or token != GATE_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token == GATE_KEY:
        user = User(username='next-ai-psych')
        return user
    else:
        user = User(username='dummy')
        return user


@app.post("/api/process-prompt")
async def process_prompt(
        prompt: dict,
        current_user: User = Depends(get_current_user)):

    if current_user.username != "next-ai-psych":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Begone you unauthorized being!",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

    # Extract the desired text from the OpenAI response
    text = response["choices"][0]["message"]["content"]

    response_data = {
        "responseText": text  # Return the response text as "responseText"
    }

    return response_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run()
    # uvicorn.run(app, host="0.0.0.0", port=8000)
