from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# FastAPIを使ってGETリクエストが飛んできたらindex.htmlを返すサーバ

app = FastAPI()

@app.get("/")
async def read_index():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
