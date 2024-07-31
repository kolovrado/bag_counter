from pipelines.proc import ObjectCounter
import os
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn

app = FastAPI()

video_processor = ObjectCounter()


@app.post('/file/')
def _count_objects( file: UploadFile = File(...),
                    directions: str = Form(description="Can objects move in both directions or not.")):
    
    contents = file.file.read()
    tmp_name = "tmp/" + file.filename   

    file.file.close()
    with open(tmp_name, "wb") as binary_file:
        binary_file.write(contents)
    
    directions = directions == "both"
    object_count = video_processor.process_video(vid_add = file.filename, allow_both = directions)

    os.remove(tmp_name)
    return {"message": f"Total objects on a video {object_count}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")