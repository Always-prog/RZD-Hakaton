import numpy as np
from stl import mesh
import uuid
import os


def create_cube(center, height, width, length):
    half_height = height / 2
    half_width = width / 2
    half_length = length / 2

    # Определение координат вершин куба
    vertices = np.array([
        [center[0] - half_width, center[1] - half_length, center[2] - half_height],  # Вершина 1
        [center[0] + half_width, center[1] - half_length, center[2] - half_height],  # Вершина 2
        [center[0] + half_width, center[1] + half_length, center[2] - half_height],  # Вершина 3
        [center[0] - half_width, center[1] + half_length, center[2] - half_height],  # Вершина 4
        [center[0] - half_width, center[1] - half_length, center[2] + half_height],  # Вершина 5
        [center[0] + half_width, center[1] - half_length, center[2] + half_height],  # Вершина 6
        [center[0] + half_width, center[1] + half_length, center[2] + half_height],  # Вершина 7
        [center[0] - half_width, center[1] + half_length, center[2] + half_height]   # Вершина 8
    ])

    # Определение граней куба
    faces = np.array([
        [0, 3, 1],  # Грань 1
        [1, 3, 2],  # Грань 2
        [0, 4, 7],  # Грань 3
        [0, 7, 3],  # Грань 4
        [4, 5, 6],  # Грань 5
        [4, 6, 7],  # Грань 6
        [5, 1, 2],  # Грань 7
        [5, 2, 6],  # Грань 8
        [2, 3, 6],  # Грань 9
        [3, 7, 6],  # Грань 10
        [0, 1, 5],  # Грань 11
        [0, 5, 4]   # Грань 12
    ])

    # Создание STL объекта
    cube_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j, vertex in enumerate(face):
            cube_mesh.vectors[i][j] = vertices[vertex]

    return cube_mesh


def create_cube_set(config):
    cube_set = []
    current_platform_center = [0, 0, -0.25]
    for i in range(len(config)):
        platform_length = float(config[i]["length"]) / 1000
        platform_width = float(config[i]["width"]) / 1000
        cargos = config[i]["cargos"]
        if i > 0:
            current_platform_center[1] += 1 + ((float(config[i - 1]["length"]) / 1000) + platform_length) / 2

        platform_cube = create_cube(
            current_platform_center,
            0.5,
            platform_width,
            platform_length)

        cube_set.append(platform_cube)

        for j in range(len(cargos)):
            cargo_length = float(cargos[j]["length"]) / 1000
            cargo_height = float(cargos[j]["height"]) / 1000
            cargo_width = float(cargos[j]["width"]) / 1000
            cargo_x = float(cargos[j]["y"]) / 1000
            cargo_y = float(cargos[j]["x"]) / 1000
            cargo_z = float(cargos[j]["z"]) / 1000

            offset = 0
            if j > 0:
                offset = cargo_y - (float(cargos[j - 1]["length"]) + float(cargos[j - 1]["x"])) / 1000

            cargo_center = [cargo_x, current_platform_center[1] + cargo_y + offset + (cargo_length - platform_length) / 2, cargo_z + cargo_height / 2]
            cargo_cube = create_cube(cargo_center, cargo_height, cargo_width, cargo_length)
            platform_cube = mesh.Mesh(np.concatenate([platform_cube.data, cargo_cube.data]))

        cube_set.append(platform_cube)

    combined_mesh = mesh.Mesh(np.concatenate([cube.data for cube in cube_set]))
    # Сохранение STL файла
    guid = uuid.uuid4()
    combined_mesh.save(f"{guid}.stl")
    data = None
    with open(f"{guid}.stl", "rb") as f:
        data = f.read()
    os.remove(f"{guid}.stl")
    return data
