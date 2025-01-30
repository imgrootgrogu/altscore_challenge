from fastapi import FastAPI, Response
import random

app = FastAPI()


SYSTEM_CODES = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}


damaged_system = random.choice(list(SYSTEM_CODES.keys()))
@app.get("/")
def home():
    return {"message": "API is running. Use /status then /repair-bay, to access /teapot: use curl or python requests "}


@app.get("/status")
def get_status():
    return {"damaged_system": damaged_system}


@app.get("/repair-bay")
def get_repair_bay():
    repair_code = SYSTEM_CODES[damaged_system]
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
        <div class="anchor-point">{repair_code}</div>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")

@app.post("/teapot")
def get_teapot():
    return Response(content="I'm a teapot", status_code=418)

