# change the base image with the one that contains the cuda toolkit compatible with your machine
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
WORKDIR /app
VOLUME ./out

# install requirements
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
RUN apt-get update && apt-get install python3-tk ffmpeg libsm6 libxext6  -y

# entrypoint is uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
