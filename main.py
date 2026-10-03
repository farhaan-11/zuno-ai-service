from fastapi import FastAPI
import os
from dotenv import load_dotenv
app = FastAPI()


load_dotenv()



@app.get("/")
def read_root():
	return {"message": "Zuno AI service is running"}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT")))
