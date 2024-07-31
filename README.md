# Bags counter

## 1. Build server:

```bash
sudo docker build . --tag trck
```

## 2. Run server:

```bash
bash run_api.sh
```

## 3. Use swagger:

```bash
http://127.0.0.1:8000/docs -> /file/ -> "Try it out"
```

Or send request:

```bash
import requests

url = "http://0.0.0.0:8000/file/"
files = {'file': open('video_2024-06-03_15-38-55.mp4', 'rb')}
# info about allowed directions of moving
# both or one
data={"directions": "one"}
res = requests.post(url, data = data, files=files)

res.json()['message'] returns message with counted bags.
```

Folder ***out*** contains output processed video. Name consists of two parts, number of bags and original filename.

# Additional docs

***Extract frames.ipynb*** - extract eacn n-th frame from the video

***train.ipynb*** - train algorithm

***Remote request.ipynb*** - Request to the working server
