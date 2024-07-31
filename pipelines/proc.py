import os
from shutil import move
import cv2
from ultralytics import YOLO, solutions

class ObjectCounter():
    def __init__(   self,
                    checkpoint = "weights/Yolo8n_best.pt"):
        
        self.model = YOLO(checkpoint)

    def process_video(  self,
                        vid_add: str = None,
                        allow_both: bool = False):

        if vid_add is None:
            return None
        cap = cv2.VideoCapture("tmp/" + vid_add)
        assert cap.isOpened(), "Error reading video file"
        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

        # Define region points
        region_points = [(150, 75), (400, 75), (400, 250), (150, 250)]

        # Video writer
        tmp_name = f"{vid_add.split('.')[0]}_object_counting_output.avi"
        video_writer = cv2.VideoWriter("tmp/" + tmp_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        # Init Object Counter
        counter = solutions.object_counter.ObjectCounter(
            view_img= False,
            reg_pts=region_points,
            classes_names=self.model.names,
            draw_tracks=True,
            line_thickness=2,
        )

        # i = 0
        # Analyze each frame
        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break
            tracks = self.model.track(im0, persist=True, show=False, verbose=False)
            
            im0 = counter.start_counting(im0, tracks)
            video_writer.write(im0)
            # cut video for testing purposes
            # i+=1
            # if i == 150:
            #     break
        
        cap.release()
        video_writer.release()

        if len(counter.count_ids) != 0:
            if allow_both:
                object_count = counter.count_ids[-1]
            else:
                object_count = counter.count_ids[-1] - counter.in_counts
        else:
            object_count = 0

        # Save video with proper name in proper place
        out_name = f"{object_count}_bags_{vid_add.split('.')[0]}.avi"

        os.rename("tmp/" + tmp_name, "tmp/" + out_name)
        move( "tmp/" + out_name, "out/" + out_name)

        return object_count