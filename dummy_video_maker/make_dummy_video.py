import cv2
import os

def make_dummy_video(image_path, save_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Can't read img {}".format(image_path))

    img = cv2.resize(img, (800, 600))
    height, width, layers = img.shape

    video = cv2.VideoWriter(save_path, 0, 1, (width,height))
    video.write(img)

    video.release()

if __name__ == "__main__":
    make_dummy_video("../data/0/image.png", "../data/0/video.avi")
