import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import APITimeoutError, OpenAI, OpenAIError

from schemas import AskRequest, AskResponse

app = FastAPI()

load_dotenv()
logger = logging.getLogger(__name__)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")

client = OpenAI(api_key=api_key)


@app.get("/")
def read_root():
    return {"message": "Zuno AI service is running"}


@app.post("/ask", response_model=AskResponse)
def ask_question(body: AskRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": body.question}],
        )
    except APITimeoutError as error:
        logger.exception("OpenAI request timed out")
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again.",
        ) from error
    except OpenAIError as error:
        logger.exception("OpenAI request failed")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not process the request.",
        ) from error
    except Exception as error:
        logger.exception("Unexpected error while generating an answer")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        ) from error

    if not response.choices or not response.choices[0].message.content:
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an empty response.",
        )

    return {
        "answer": response.choices[0].message.content,
        "message": "AI response",
    }


# import uvicorn

# uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT",8000)))
