from .HikCamera.HikCamera import *
from .Colors import *
from .ArucoDetector import *
from .FrameGrabberConfig import *
from .WebCamera import *

import logging
logger = logging.getLogger()


class FrameGrabber:

    CALIBRATION_DATA_NAME = 'calibration_data.npy'
    CALIBRATION_DATA_PATH = os.path.join('/', 'config', CALIBRATION_DATA_NAME)

    def __init__(self):
        logger.info('Initializing frame grabber')
        opencv_cuda_devices = cv2.cuda.getCudaEnabledDeviceCount()
        if opencv_cuda_devices > 0:
            logging.info(f"OpenCV is using CUDA GPU accelerator with {opencv_cuda_devices} devices")
            self.use_cuda = True
        else:
            logger.info('OpenCV is built without CUDA support and is using CPU accelerator')
            self.use_cuda = False
        self.config = FrameGrabberConfig()
        self.M = None
        try:
            self.M = np.load(self.CALIBRATION_DATA_PATH)
            logger.info('Calibration data loaded')
        except Exception:
            logger.error('Calibration data not found')
            pass

        logger.info('Initializing camera')
        if self.config['camera_type'] == 'hik':
            self.camera = Camera()
        else:
            self.camera = Webcamera(self.config['webcamera_address'])
        self.camera.open()
        self.camera.set_exposure(self.config['exposure'])

        self.aruco = ArucoDetector()

    def uncalibrate(self):
        self.M = None
#TODO: REMOVE CALIBRATION FILE FROM MEMORY
        os.remove(self.CALIBRATION_DATA_PATH)
        logger.info('Calibration data removed')

    def calibrate(self):
        logger.info('Begin calibration')
        gray = self.camera.get_frame()
        markers = self.aruco.detectMarkers(gray)

        logger.info(f'Found {len(markers)} markers')
        if len(markers) >= 4:
            start_p = np.float32(
                [markers[1].topRight, markers[3].bottomRight, markers[2].bottomLeft, markers[0].topLeft])
            dest_p = np.float32([[0, 0], [self.config['markers_x_distance'], 0], [
                                self.config['markers_x_distance'], self.config['markers_y_distance']], [0, self.config['markers_y_distance']]])
            self.M = cv2.getPerspectiveTransform(start_p, dest_p)
            np.save(self.CALIBRATION_DATA_PATH, self.M)
            logger.info('Calibration data updated')

    def set_exposure(self, exposure):
        self.camera.set_exposure(exposure)
        self.config['exposure'] = exposure

    def get_exposure(self):
        return self.config['exposure']

    def get_frame(self):
        start_time = time.time()
        gray = self.camera.get_frame()
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        try:
            h,  w = frame.shape[:2]
            if self.use_cuda:
                gpu_frame = cv2.cuda_GpuMat()
                gpu_frame.upload(frame)
                # Создание GPU-матрицы преобразования
                gpu_M = self.M.astype(np.float32)  # Убедитесь, что матрица имеет тип float32
                size = (self.config['markers_x_distance'], self.config['markers_y_distance'])
                result_gpu = cv2.cuda.warpPerspective(gpu_frame, gpu_M, size)
                result = result_gpu.download()
            else:
                result = cv2.warpPerspective(frame, self.M, [self.config['markers_x_distance'], self.config['markers_y_distance']])
            
            # Рисуем FPS на изображении
            cv2.putText(result,f"FPS: {(1.0 / (time.time() - start_time)):.2f}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0, 255, 0),2)
            return result
        except Exception as e :
            logger.debug(e)
            markers = self.aruco.detectMarkers(frame)
            for id, marker in markers.items():
                cv2.drawMarker(frame, marker.center, COLOR_PINK, cv2.MARKER_CROSS, 15, 8)
                points = np.array([marker.topLeft, marker.topRight, marker.bottomRight, marker.bottomLeft], np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(frame, [points], isClosed=True, color=COLOR_PINK, thickness=2)

                        
            # Рисуем FPS на изображении
            cv2.putText(frame,f"FPS: {(1.0 / (time.time() - start_time)):.2f}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0, 255, 0),2)
            return frame


if __name__ == '__main__':
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    cv2.namedWindow("Frame", cv2.WINDOW_FREERATIO)
    framer = FrameGrabber()
    while True:
        frame = framer.get_frame()
        markers = framer.aruco.detectMarkers(frame)
        if len(markers) > 0:
            for id, marker in markers.items():
                cv2.drawMarker(frame, marker.center, COLOR_PINK,
                               cv2.MARKER_CROSS, 15, 8)
        cv2.imshow("Frame", frame)
        cmd = cv2.waitKey(1)
        if cmd == ord('c'):
            framer.calibrate()
        if cmd == ord('q'):
            break
