import cv2
import numpy as np
import logging
logger = logging.getLogger()

class ArucoMarker():
    def __init__(self, id, center, corners):
        self.id = id
        self.center = center
        [self.topLeft, self.topRight, self.bottomRight, self.bottomLeft] = corners

class ArucoDetector:    
    def __init__(self):
        self.use_cuda = cv2.cuda.getCudaEnabledDeviceCount() > 0
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)

    def detectMarkers(self, frame):
        try:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            corners, ids, rejected = self.detector.detectMarkers(gray_frame)

            markers = {}
            if ids is not None:
                ids = ids.flatten()
                for (markerCorner, markerID) in zip(corners, ids):
                    corners_arr = markerCorner.reshape((4, 2)).astype(int)
                    topLeft, topRight, bottomRight, bottomLeft = corners_arr
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    logger.info(f"ArUco marker ID: {markerID}")
                    markers[markerID] = ArucoMarker(markerID, [cX, cY], [topLeft, topRight, bottomRight, bottomLeft])
            else:
                logger.info("No markers detected")
            return markers

        except Exception as e:
            logger.error(e)
            return {}

if __name__ == '__main__':
    from HikCamera.HikCamera import *
    from Colors import *
    cam = Camera()
    cam.open()
    e = 10000
    cam.set_exposure(e)
    cv2.namedWindow("Frame", cv2.WINDOW_FREERATIO)

    aruco = ArucoDetector()

    while True:
        gray = cam.get_frame()
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        markers = aruco.detectMarkers(gray)

        if len(markers) > 0:
            for id, marker in markers.items():
                cv2.drawMarker(frame, marker.center, COLOR_PINK, cv2.MARKER_CROSS, 5, 8)

        cv2.imshow("Frame", frame)
        cmd = cv2.waitKey(1)
