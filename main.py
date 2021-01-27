import cv2
import numpy as np


HEIGHT = 1200
WIDTH = 1600
DOMAIN_Y = 1.5
DOMAIN_X = 2.
STEPS = 30


def check_divergence(x, y):
    current_x = 0
    current_y = 0
    for n in range(STEPS):
        next_x = current_x ** 2 - current_y ** 2 + x
        next_y = 2 * current_x * current_y + y
        distance = (next_x ** 2 + next_y ** 2) ** 0.5
        if distance > 2.:
            return n, distance
        current_x, current_y = next_x, next_y
    return -1, None


def main():
    min_max = [[float('inf'), float('-inf')] for _ in range(STEPS)]
    n_divs = np.empty((HEIGHT, WIDTH), dtype=np.int8)
    distances = np.empty((HEIGHT, WIDTH))
    img = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for h in range(HEIGHT):
        for w in range(WIDTH):
            x = DOMAIN_X / WIDTH * (w * 2 + 1) - DOMAIN_X
            y = DOMAIN_Y / HEIGHT * (h * 2 + 1) - DOMAIN_Y
            n_divs[h][w], distances[h][w] = check_divergence(x, y)
            if n_divs[h][w] == -1:
                continue
            if min_max[n_divs[h][w]][0] > distances[h][w]:
                min_max[n_divs[h][w]][0] = distances[h][w]
            if min_max[n_divs[h][w]][1] < distances[h][w]:
                min_max[n_divs[h][w]][1] = distances[h][w]

    for h in range(HEIGHT):
        for w in range(WIDTH):
            if n_divs[h][w] == -1:
                img[h][w][:] = 0
            else:
                criteria = 255. / STEPS * n_divs[h][w]
                dis_range = min_max[n_divs[h][w]][1] - min_max[n_divs[h][w]][0]
                dis = min_max[n_divs[h][w]][1] - distances[h][w]
                offset = 255. / STEPS * (dis / dis_range)
                img[h][w][1] = int(criteria + offset)
                img[h][w][0::2] = 0

    cv2.imwrite('mandelbrot.png', img)


if __name__ == '__main__':
    main()
