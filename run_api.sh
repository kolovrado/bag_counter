sudo docker run -d --gpus=all  --restart=always --ipc=host --network=host\
 -v $(pwd):/app \
 trck:latest \

