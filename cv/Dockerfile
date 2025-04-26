FROM robowizardspb/jetson-nano-ultralytics-opencv-cuda:1.0.0
RUN python3.8 -m pip install fastapi[standard]
WORKDIR /app
COPY . .
RUN dpkg -i hikcamsdk.deb
ENV MVCAM_COMMON_RUNENV=/opt/MVS/lib LD_LIBRARY_PATH=/opt/MVS/lib/64:/opt/MVS/lib/32:$LD_LIBRARY_PA$
EXPOSE 8001
ENTRYPOINT ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
