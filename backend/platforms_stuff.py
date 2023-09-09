import functions_for_boxes as bx

#Test_cargo_set
lst_cargo_veight = [6670, 4085, 395, 1865]
lst_cargo_len = [3650, 3870, 1080, 4100]
lst_cargo_height = [1500, 1020, 390, 1865]
lst_cargo_width = [3320, 2890, 1580, 1720]

#Test_cargo_set_2

cargo_list = []

def create_platforms_with_cargo(cargo):
    MAX_MASS = 50000
    mass = 0
    cargo_len = 0
    types_platform = {"13-401": (70, (13400, 2770), 20.92, 1810, 36841000),
                      "13-926": (73, (18400, 2830), 27, 1807, 51789000)}

    x_cargo = -1 * (13400 / 2)
    y_cargo = 0
    platform = []
    cargo_coords = []
    i = 0
    take_new_platform = False
    max_len = 13400
    x_cargo += cargo[0][1][0] / 2
    cargo_coords.append((x_cargo, y_cargo))
    while mass < MAX_MASS and cargo_len < 18400 and i < len(cargo):
        if mass + cargo[i][0] < MAX_MASS and cargo_len + cargo[i][1][0] + bx.SPACE < max_len:
            mass += cargo[i][0]
            cargo_len += cargo[i][1][0] + bx.SPACE
            x_cargo += cargo[i][1][0] + bx.SPACE
            if i > 1:
                cargo_coords.append((x_cargo, y_cargo))
        else:
            print("Ограничения по вместимости.")
            break


        #print(f"Общая масса равна: {mass}. Общая длинна: {cargo_len}")
        i += 1

    if cargo_len <= 13400:
        platform_type = "13-401"
    elif cargo_len <= 18400:
        platform_type = "13-926"
    else:
        print("Критическая ошибка.")
        return False

    #print(cargo_coords)
    for i in range(0, len(cargo) - 1):
        platform.append((cargo[i],cargo_coords[i]))

    return platform, platform_type

def gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height):
    res = []
    for i in range(0, len(lst_cargo_height)):
        res.append(tuple((lst_cargo_len[i], lst_cargo_width[i], lst_cargo_height[i])))
    return res


def info_cargo(lst_cargo_veight, lst_cargo_len, lst_cargo_width, lst_cargo_height):
    res = []
    cargo_gab = gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height)
    for i in range(0, len(lst_cargo_len)):
        res.append(tuple((lst_cargo_veight[i], cargo_gab[i])))

    return res


def veight(cargo):
    return -cargo[0]

def square(cargo):
    print(cargo[1][0] * cargo[1][1])
    return(-cargo[1][0] * cargo[1][1])


if __name__ == '__main__':
    cargo = info_cargo(lst_cargo_veight, lst_cargo_len, lst_cargo_width, lst_cargo_height)
    #my_lst.sort(key=square)
    print(cargo)
    print('-' * 20)
    print(create_platforms_with_cargo(cargo))