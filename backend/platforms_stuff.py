import functions_for_boxes as bx

#Test_cargo_set
lst_cargo_veight = [6670, 4085, 395, 1865]
lst_cargo_len = [3650, 3870, 1080, 4100]
lst_cargo_height = [1500, 1020, 390, 1865]
lst_cargo_width = [3320, 2890, 1580, 1720]

cargo_list = []

def create_train():

    MAX_MASS = 50000


def gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height):
    res = []
    for i in range(0, len(lst_cargo_height) - 1):
        res.append(tuple((lst_cargo_len[i], lst_cargo_width[i], lst_cargo_height[i])))
    return res


def info_cargo(lst_cargo_veight, lst_cargo_len, lst_cargo_width, lst_cargo_height):


if __name__ == '__main__':
    print(gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height))