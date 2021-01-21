from fastapi import Body, Header, HTTPException, status, Response
from typing import Optional


from Server import app
from Server.db.schemas.userschema import AddTank, RetriveData, AppData
from Server.db.controllers.tankHandlers import addNewTank
from Server.db.controllers.influxHandlers import retriveData
from Server.db.controllers.appHandlers import getAppData
from Server.views.userView import setToken


@app.post("/app/addtank")
async def addTank(response: Response, Authorization: Optional[str] = Header(None), body: AddTank = Body(...)):
    user = await token_check(Authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tank = dict()
    tank["device_id"] = body.device_id
    tank["fish_names"] = body.fish_names
    tank["fish_count"] = body.fish_count
    tank["height"] = body.height
    tank["lenght"] = body.lenght
    tank["width"] = body.width
    if (await addNewTank(tank, body.email)):
        access_token = setToken(body.email)
        response.headers["Authorization"] = "Bearer "+access_token
        return{"status": True}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.post("/app/retrivedata")
async def retriveTankData(response: Response, Authorization: Optional[str] = Header(None), body: RetriveData = Body(...)):
    user = await token_check(Authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = setToken(body.email)
    response.headers["Authorization"] = "Bearer "+access_token
    data = await retriveData(body.device_id, body.day)
    return {"status": True, "data": data}


@app.post("/app/getdevicedata")
async def retriveDevicesData(response: Response, Authorization: Optional[str] = Header(None), body: AppData = Body(...)):
    user = await token_check(Authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = await getAppData(body.email)
    access_token = setToken(body.email)
    response.headers["Authorization"] = "Bearer "+access_token
    return {"status": True, "data": data}
