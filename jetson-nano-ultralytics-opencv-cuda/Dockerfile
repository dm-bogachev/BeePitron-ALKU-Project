FROM ultralytics/ultralytics:latest-jetson-jetpack4
ARG OPENCV_VERSION=4.11.0
RUN apt-get update
RUN apt-get install -y unzip gcc
WORKDIR /opt
RUN apt-key adv --fetch-key http://repo.download.nvidia.com/jetson/jetson-ota-public.asc
RUN echo 'deb https://repo.download.nvidia.com/jetson/common r32.6 main\n \
deb https://repo.download.nvidia.com/jetson/t210 r32.6 main' > /etc/apt/sources.list.d/nvidia-l4t-apt-source.list
RUN apt-get update && apt-get install -y nvidia-cuda nvidia-cudnn8
RUN wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip 
RUN unzip $OPENCV_VERSION.zip 
RUN rm $OPENCV_VERSION.zip
RUN wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip
RUN unzip ${OPENCV_VERSION}.zip 
RUN rm ${OPENCV_VERSION}.zip
RUN export CUDA_ROOT=/usr/local/cuda
RUN mkdir opencv-${OPENCV_VERSION}/build
WORKDIR /opt/opencv-${OPENCV_VERSION}/build
RUN apt-get install -y cmake build-essential
RUN cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-${OPENCV_VERSION}/modules \
    -D BUILD_opencv_python3=ON \
    -D WITH_CUDA=ON \
    -D WITH_CAROTENE=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_DOCS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D CUDA_ARCH_BIN="5.3" \
    -D CUDA_ARCH_PTX="" \
    ..
RUN make -j"$(nproc)"
RUN python3.8 -m pip uninstall -y opencv-python
RUN make install 
RUN ldconfig 
RUN rm -rf /opt/opencv-${OPENCV_VERSION} 
RUN rm -rf /opt/opencv_contrib-${OPENCV_VERSION}
RUN cp -r /usr/local/lib/python3.8/site-packages/cv2/ /usr/local/lib/python3.8/dist-packages/
