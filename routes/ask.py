import logging

from fastapi import APIRouter, HTTPException
from openai import APITimeoutError, OpenAIError

from config import MODEL_NAME, client
from schemas import AskRequest, AskResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(body: AskRequest):
    logger.info("Received question (%d characters)", len(body.question))

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
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

    logger.info("Answer generated successfully")

    return {
        "answer": response.choices[0].message.content,
        "message": "AI response",
    }
