from fastapi import FastAPI
from fastapi.responses import Response


app = FastAPI()


@app.route('/')
async def home(request):
    return Response("hello")



