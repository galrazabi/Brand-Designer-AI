import csv
import random, pickle


shapes = [
    "Circle", "Square", "Triangle", "Rectangle", "Pentagon", "Hexagon", "Octagon",
    "Rhombus", "Trapezoid", "Parallelogram", "Ellipse", "Oval", "Cylinder", "Cone",
    "Sphere", "Cube", "Pyramid", "Torus", "Triangular Prism", "Rectangular Prism",
    "Pentagonal Prism", "Hexagonal Prism", "Octagonal Prism", "Dodecahedron", "Icosahedron"
]
products = ["tote bag", "take away cup", "notebook", "baseball hat"]

def get_color_from_csv():
    colors_list = []
    with open("./data/color_names.csv", "r") as file: 
        csv_reader = csv.reader(file)
        next(csv_reader) 
        for row in csv_reader:
            color = row[0]
            color = color.strip()
            colors_list.append(color)
    return colors_list


def get_random_colors():
    colors_list = get_color_from_csv()
    random_colors = random.sample(colors_list, 3)
    return random_colors


def get_random_shapes():
    random_shape = random.sample(shapes, 1)
    return random_shape[0]


def read_logos_file():
    logos_list = []
    with open('./data/out.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for line in csv_reader:
                logos_list.append(line)

    return logos_list


def make_pickle_file(data: list, file_path: str):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def load_pickle_file(file_path):
    with open(file_path, 'rb') as file:
        loaded_data = pickle.load(file)
    return loaded_data
