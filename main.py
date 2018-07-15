import cv2
import numpy as np

import matplotlib.pyplot as plt
import pygame

window = "Color Tracking"


def main():
    cap = cv2.VideoCapture(0)

    cap.set(3, 50)
    cap.set(4, 50)

    (width, height) = (cap.get(3), cap.get(4))

    pygame.init()
    drum = pygame.mixer.Sound("drum.wav")
    drum2 = pygame.mixer.Sound("drum2.wav")

    drum.set_volume(0.3)

    soundR = False
    soundG = False

    r = 7

    print(f'{width}x{height}')
    while True:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        p1 = (0, int(4 * height / 5))
        p2 = (int(width), int(height))
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 1)

        # Red
        low = np.array([140, 150, 50])
        high = np.array([180, 255, 255])

        imgMask = cv2.inRange(hsv, low, high)
        count = 0
        (xr, yr) = (0, 0)
        for i, _ in enumerate(imgMask):
            for j, c in enumerate(_):
                if (imgMask[i, j] == 255):
                    xr += j
                    yr += i
                    count += 1

        if count != 0:
            xr /= count
            yr /= count
            cv2.circle(frame, (int(xr), int(yr)), r, (255, 0, 255), -1)

        # Green
        low = np.array([40, 50, 50])
        high = np.array([80, 255, 255])

        imgMask = cv2.inRange(hsv, low, high)
        count = 0
        (xg, yg) = (0, 0)
        for i, _ in enumerate(imgMask):
            for j, c in enumerate(_):
                if (imgMask[i, j] == 255):
                    xg += j
                    yg += i
                    count += 1

        if count != 0:
            xg /= count
            yg /= count
            cv2.circle(frame, (int(xg), int(yg)), r, (0, 0, 255), -1)

        if yr > p1[1] - r:
            if not soundR:
                drum.play()
                soundR = True
        else:
            soundR = False

        if yg > p1[1] - r:
            if not soundG:
                drum2.play()
                soundG = True
        else:
            soundG = False

        frame = cv2.resize(frame, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(f'{window} Original', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
