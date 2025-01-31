from fastapi import FastAPI, Response, Query
import random
import numpy as np


app = FastAPI()


SYSTEM_CODES = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

pressure_values = np.array([0.05, 10])  # MPa
specific_volume_liquid = np.array([0.00105, 0.0035])  # m³/kg (v_f values)
specific_volume_vapor = np.array([30.00, 0.0035])  # m³/kg (v_g values)

# Gas constant for water vapor
R = 0.4615  # kJ/kg·K

@app.get("/phase-change-diagram")
async def compute_specific_volumes(
    pressure: float = Query(..., description="Pressure in MPa"),
    T: float = Query(None, description="Temperature in Celsius (optional, defaults to 40°C)")):
    """
    Computes specific volumes of liquid and vapor given pressure and temperature.
    - Returns an error message if T <= 30°C.
    - Uses interpolation for volumes below the critical point.
    - Applies the ideal gas law for vapor if T > T_sat_critical.
    """
    if T is None:
        T = 40
    if T <= 30:
        return {"message": "Repair robot will probe only T > 30°C"}

    v_f = np.interp(pressure, pressure_values, specific_volume_liquid)
    v_g = np.interp(pressure, pressure_values, specific_volume_vapor)


    T_sat_critical = 500  


    if T > T_sat_critical:
        v_g = (R * T) / pressure  

    return {
        "specific_volume_liquid": round(float(v_f), 5),
        "specific_volume_vapor": round(float(v_g), 5)
    }

damaged_system = random.choice(list(SYSTEM_CODES.keys()))
@app.get("/")
def home():
    return {"message": "API is running. Use /status then /repair-bay, to access /teapot: use curl or python requests. /phase-change-diagram?pressure=() or /phase-change-diagram?pressure=()&T=() "}


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

