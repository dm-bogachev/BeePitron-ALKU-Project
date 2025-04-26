import logging

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

logging.info("Initialize Robot class")
from Robot.Robot import Robot
robot = Robot()
robot.start()
logging.info("Robot class initialize complete")

logging.info("Starting FastAPI")
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
logging.info("FastAPI starting complete")

# Robot API
@app.get("/robot/connection")
def robot_status():
    return {"connected": robot.connection.connected}

@app.get("/robot/pick")
def robot_pick(class_id: str, x: float, y: float, a: float = None):
    if a is not None:
        return robot.send_pick(class_id, (x, y, a))
    else:
        return robot.send_pick(class_id, (x, y) )

@app.get("/robot/measurement")
def robot_measurement(result: bool):
    return robot.send_measurement_request(result)