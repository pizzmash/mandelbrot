import cv2
import numpy as np
from tqdm import tqdm


HEIGHT = 2160
WIDTH = 3840
DOMAIN_Y = 1.125
DOMAIN_X = 2.
STEPS = 256


def check_divergence(x, y):
    current_x = 0
    current_y = 0
    for n in range(STEPS):
        next_x = current_x ** 2 - current_y ** 2 + x
        next_y = 2 * current_x * current_y + y
        distance = (next_x ** 2 + next_y ** 2) ** 0.5
        if distance > 2.:
            return n
        current_x, current_y = next_x, next_y
    return -1


def main():
    img = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for h in tqdm(range(HEIGHT)):
        for w in range(WIDTH):
            x = DOMAIN_X / WIDTH * (w * 2 + 1) - DOMAIN_X
            y = DOMAIN_Y / HEIGHT * (h * 2 + 1) - DOMAIN_Y
            n_div = check_divergence(x, y)
            if n_div == -1:
                img[h][w][:] = 0
            else:
                img[h][w][1] = int(255. / STEPS * n_div)
                img[h][w][0::2] = 0

    cv2.imwrite('mandelbrot.png', img)


if __name__ == '__main__':
    main()
