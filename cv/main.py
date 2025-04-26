import logging

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

import cv2

logging.info("Initialize Vision class")
from Vision.Vision import Vision
vision = Vision()
vision.start()
logging.info("Vision class initialize complete")

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


def generate_frames():
    while True:
        frame = vision.get_display_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Vision API
@app.get("/vision/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/vision/get_models")
def get_models():
    return vision.get_models()

@app.get("/vision/set_model")
def set_model(model: str):
    if model in vision.get_models():
        vision.set_model(model)
        return {"model_set": model}
    else:
        return {"error": "Model not found"}

@app.get("/vision/get_model")
def get_model():
    return {"model": vision.current_model}

@app.get("/vision/get_confidence")
def get_confidence(model: str):
    if model in vision.get_models():
        return {"confidence": vision.config['minimal_confidences'][model]}
    else:
        return {"error": "Model not found"}

@app.get("/vision/set_confidence")
def set_confidence(model: str, confidence: float):
    if model in vision.get_models():
        minimal_confidences = vision.config['minimal_confidences']
        minimal_confidences[model] = confidence
        vision.config['minimal_confidences'] = minimal_confidences
        return {"confidence_set": confidence}
    else:
        return {"error": "Model not found"}

@app.get("/vision/get_objects")
def get_objects():
    return vision.objects

@app.get("/vision/get_display_box")
def get_display_box():
    return {"display_box": vision.config['display_box']}

@app.get("/vision/set_display_box")
def set_display_box(display_box: bool):
    vision.config['display_box'] = display_box
    return {"display_box": display_box}

@app.get("/vision/get_display_pose")
def get_display_pose():
    return {"display_pose": vision.config['display_pose']}

@app.get("/vision/set_display_pose")
def set_display_pose(display_pose: bool):
    vision.config['display_pose'] = display_pose
    return {"display_pose": display_pose}

@app.get("/vision/get_display_coordinates")
def get_display_coordinates():
    return {"display_coordinates": vision.config['display_coordinates']}

@app.get("/vision/set_display_coordinates")
def set_display_coordinates(display_coordinates: bool):
    vision.config['display_coordinates'] = display_coordinates
    return {"display_coordinates": display_coordinates}

@app.get("/vision/get_display_confidence")
def get_display_confidence():
    return {"display_confidence": vision.config['display_confidence']}

@app.get("/vision/set_display_confidence")
def set_display_confidence(display_confidence: bool):
    vision.config['display_confidence'] = display_confidence
    return {"display_confidence": display_confidence}

# FrameGrabber API
@app.get("/framegrabber/set_exposure")
def set_exposure(exposure: int):
    if 162 <= exposure <= 900000:
        vision.frame_grabber.set_exposure(exposure)
        return {"exposure_set": exposure}
    else:
        return {"error": "Exposure value out of range. Must be between 162 and 900000."}

@app.get("/framegrabber/get_exposure")
def get_exposure():
    return {"exposure": vision.frame_grabber.get_exposure()}

@app.get("/framegrabber/get_markers_x_distance")
def get_markers_x_distance():
    return {"markers_x_distance": vision.frame_grabber.config['markers_x_distance']}

@app.get("/framegrabber/get_markers_y_distance")
def get_markers_y_distance():
    return {"markers_y_distance": vision.frame_grabber.config['markers_y_distance']}

@app.get("/framegrabber/set_markers_x_distance")
def set_markers_x_distance(distance: int):
    if 0 <= distance <= 900000:
        vision.frame_grabber.config['markers_x_distance'] = distance
        return {"markers_x_distance": distance}
    else:
        return {"error": "Distance value out of range. Must be between 0 and 900000."}

@app.get("/framegrabber/set_markers_y_distance")
def set_markers_y_distance(distance: int):
    if 0 <= distance <= 900000:
        vision.frame_grabber.config['markers_y_distance'] = distance
        return {"markers_y_distance": distance}
    else:
        return {"error": "Distance value out of range. Must be between 0 and 900000."}

@app.get("/framegrabber/calibrate")
def calibrate():
    vision.frame_grabber.calibrate()
    return {"calibrated": True}

@app.get("/framegrabber/uncalibrate")
def uncalibrate():
    vision.frame_grabber.uncalibrate()
    return {"calibrated": False}

@app.get("/framegrabber/get_display_width")
def get_display_width():
    return {"display_width": vision.frame_grabber.config["display_width"]}

@app.get("/framegrabber/set_display_width")
def set_display_width(display_width: int):
    vision.frame_grabber.config['display_width'] = display_width
    return {"display_width": display_width}


@app.get("/framegrabber/get_display_height")
def get_display_height():
    return {"display_height": vision.frame_grabber.config["display_height"]}

@app.get("/framegrabber/set_display_height")
def set_display_height(display_height: int):
    vision.frame_grabber.config['display_height'] = display_height
    return {"display_height": display_height}
# @app.get("/vision/set_display_coordinates")
# def set_display_coordinates(display_coordinates: bool):
#     vision.config['display_coordinates'] = display_coordinates
#     return {"display_coordinates": display_coordinates}

# @app.get("/vision/get_display_confidence")
# def get_display_confidence():
#     return {"display_confidence": vision.config['display_confidence']}
