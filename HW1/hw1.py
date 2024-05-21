from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

vid_cap = cv2.VideoCapture("argoverse.mp4")

# video recorder setting
width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vid_cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_vid = cv2.VideoWriter("dst.mp4", fourcc, fps, (width, height))

if __name__ == "__main__":

    frame_counter = 0

    # get car's id
    target_name = "car"
    car_class_id = None
    for id, name in model.names.items():
        if name == target_name:
            car_class_id = id
            break

    while True:
        ret, frame = vid_cap.read()
        frame_counter += 1
        if ret:
            results = model(frame)

            # filter car class
            for result in results:
                filtered_boxes = []
                for box in result.boxes:
                    if box.cls == car_class_id:
                        filtered_boxes.append(box)
                result.boxes = filtered_boxes

            annotated_frame = results[0].plot()
            cv2.imshow("view", annotated_frame)

            output_vid.write(annotated_frame)  # output video

            ##### replay video #####
            # if frame_counter == vid_cap.get(cv2.CAP_PROP_FRAME_COUNT):
            #     frame_counter = 1
            #     vid_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(1) == ord("q"):
            break
        elif frame_counter == vid_cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break

vid_cap.release()
cv2.destroyAllWindows()
