import matplotlib.pyplot as plt
import matplotlib.image as image
import numpy as np

FILENAME = 'teapot.obj'
vertexes = []
facets = []
N = 1600
k = 0
x_min, y_min = (999999, 999999)
x_max, y_max = (-999999, -999999)
end_of_circle = -99999
scale = []

def fill_facets_and_vertex():
    global vertexes, facets
    file = open(FILENAME, 'r')
    for line in file:
        line = line.replace("\n", " ")
        if line.startswith('v'):
            vertexes.append(line.split(" ")[1:3])
            find_min_and_max_coord(line.split(" ")[1:3])
        if line.startswith('f'):
            facets.append(line.split(" ")[1:4])
    global end_of_circle
    if (x_max - x_min) < (y_max - y_min):
        end_of_circle = x_max - x_min
    else:
        end_of_circle = y_max - y_min
    np.array(facets)
    np.array(vertexes)

def find_min_and_max_coord(vertexes):
    global x_min, x_max, y_max, y_min
    if float(vertexes[0]) > x_max:
        x_max = float(vertexes[0])
    elif float(vertexes[0]) < x_min:
        x_min = float(vertexes[0])
    if float(vertexes[1]) > y_max:
        y_max = float(vertexes[1])
    elif float(vertexes[1]) < y_min:
        y_min = float(vertexes[1])

def make_background():
    center_color = [255, 1, 1] #ярко-розовый
    arr = np.zeros((N, N, 3), dtype=np.uint8)
    global end_of_circle
    for x in range(N):
        for y in range(N):
            #поиск расстояния от пикселя до центра
            d = np.sqrt((x - N/2) ** 2 + (y - N/1.5) ** 2)
            if d < end_of_circle / 2 * N/9 :
                # d -= end_of_circle * N/10
            #вычисление цвета (color * (1 - d/size))
                r = center_color[0] * (1 - d/N)
                g = center_color[1] * (1 - d/N)
                b = center_color[2] * (1 - d/N)
                arr[x, y] = (r, g, b)
            else :
                arr[x, y] = (0, 0, 0)
    return arr

def calculate_scale():
    global k, vertexes, scale
    for vertex in vertexes:
        for point in vertex:
            if abs(float(point)) > k:
                k = abs(float(point))
    k *= N/30
    scale = [[k, 0],
            [0, k]]

def move(point):
    return point + N/2

def make_scaling(mtr):
    res = np.array([move(mtr[0] * scale[0][0]), move(mtr[1] * scale[1][1])])
    return res

#использовать матрицу масштабирования
def draw(base_color, img):
    global vertexes, facets, N
    for facet in facets:
        for i in range(len(facet)):
            first = make_scaling([float(vertexes[int(facet[i - 1]) - 1][0]), float(vertexes[int(facet[i - 1]) - 1][1])])
            second = make_scaling([float(vertexes[int(facet[i]) - 1][0]), float(vertexes[int(facet[i]) - 1][1])])
            draw_line(int(first[0]), int(first[1]), int(second[0]), int(second[1]), base_color, img)

def draw_line(x0, y0, x1, y1, base_color, img):
    global N
    swap = 0
    # вертикальное расстояние между текущим значением y и точным значением y для текущего x
    count_error_d_y = 0
    # угол наклона равен tg(alpha)
    dx = x1 - x0
    dy = y1 - y0
    # если первая точка правее второй
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    # если tg(alpha) > 1
    if dy > dx:
        x0, y0, x1, y1 = y0, x0, y1, x1
        swap = 1
    # если tg(alpha) < -1
    if abs(dy) > x1 - x0:
        x0, y0, x1, y1 = y1, x1, y0, x0
        swap = 1
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    # найти и нарисовать точку (x, y)
    for x in range(x0, x1 + 1):
        if swap == 1:
            # т.к поворот на 90 градусов
            img[y0, x] = base_color
        else:
            img[x, y0] = base_color
        count_error_d_y += delta_y
        if (count_error_d_y * 2 > delta_x):
            # изменяем y на sign(y1 - y0)
            y0 += 1 if y0 < y1 else -1
            count_error_d_y -= delta_x

def show(img):
    image.imsave("teapot.png", np.rot90(img))
    plt.imshow(np.rot90(img))
    plt.show()

if __name__ == "__main__":
    fill_facets_and_vertex()
    base_color = [255, 255, 255]
    img = make_background()
    calculate_scale()
    draw(base_color, img)
    show(img)