from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Zuno AI service is running"}
