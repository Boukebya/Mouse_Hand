# la vidéo fait 18 secondes, on veut la décomposer en 1000 images, 30 fps
# 18 * 30 = 540, 540 / 1000 = 0.54

factor = 0.54
import cv2
import os
import numpy as np

# créer une image de la frame touts les 0.5 frames
# Obtenir les dimensions de l'écran
screen_width, screen_height = 1920, 1080
vid = cv2.VideoCapture('none.mp4')
fps = vid.get(cv2.CAP_PROP_FPS)
print(fps)
frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_count)
success, image = vid.read()
count = 0
while success:
    if count % 2 == 0:
        cv2.imwrite(f'dataset/none/frame{count}.png', image)
    success, image = vid.read()
    count += 1
    if count % 100 == 0:
        print(count)
vid.release()
cv2.destroyAllWindows()
