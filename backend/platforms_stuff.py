import functions_for_boxes as bx

# Test_cargo_set
lst_cargo_weight = [6670, 4085, 395, 1865] * 5  # Веса грузов
lst_cargo_len = [3650, 3870, 1080, 4100] * 5  # Длинна грузов
lst_cargo_height = [1500, 1020, 390, 1865] * 5  # Высота грузов
lst_cargo_width = [3320, 2890, 1580, 1720] * 5  # Ширина грузов

cargos = [{'weight': lst_cargo_weight[i], 'length': lst_cargo_len[i], 'height': lst_cargo_height[i],
           'width': lst_cargo_width[i]} for i in range(len(lst_cargo_weight))]

# Test_cargo_set_2

cargo_list = []


def select_platforms_by_cargos(cargos):
    """
    Распределитель грузов по вагонам
    """

    LIMIT_CARGOS_MASS = 50000  # 50 ТОНН.

    types_platform = {
        "13-401": {
            'type': '13-401',  # Тип
            'weight_limit': 70,  # грузоподъёмность
            'length': 13400,  # Длинна
            'width': 2770,  # Ширина
            'mass': 20.92,  # вес вагона в тоннах
            'height_gravity': 1810,  # высота центра тяжести вагона
        },
        "13-926": {
            'type': '13-926',
            'weight_limit': 73,
            'length': 18400,
            'width': 2830,
            'mass': 27,
            'height_gravity': 1807,
        },
    }
    LIMIT_CARGO_LENGTH = max(platform['length'] for platform in types_platform.values())
    # Нужно отфильтровать все грузы которые вообще не влезают на платформу
    filter_unexpected = lambda cargo: cargo['length'] < LIMIT_CARGO_LENGTH and cargo['weight'] < LIMIT_CARGOS_MASS

    platforms = []
    current_platform_type = '13-401'
    current_cargos = []
    for cargo in filter(filter_unexpected, cargos):
        total_cargos_length = sum([c['length'] for c in current_cargos])+(len(current_cargos) * bx.SPACE)
        total_cargos_mass = sum([c['weight'] for c in current_cargos])

        # Если груз становиться слишком тяжелым - добавляем на новую платформу
        if total_cargos_mass + cargo['weight'] > LIMIT_CARGOS_MASS:
            platforms.append({
                **types_platform[current_platform_type],
                'cargos': current_cargos.copy(),
            })
            current_cargos = []
            continue

        # Если груз не подходит по длине - проверить есть ли вообще платформа способная его вместить
        # Если нет, создать новую платформу которая бы его вместила
        if total_cargos_length + cargo['length'] > types_platform[current_platform_type]['length']:
            # Поиск платформы способной вместить еще один груз
            can_be_platform = None  # Платформа, способная вместить груз
            for platform_type, platform_info in types_platform.items():
                if platform_info['length'] > total_cargos_length + cargo['length']:
                    can_be_platform = platform_type
                    break
            if can_be_platform:  # Если найдена более вместительная платформа - используем.
                current_platform_type = can_be_platform
            else:  # Если нет более вместительной платформы - сохраняем нашу прошлую, добавляем новую.
                platforms.append({
                    **types_platform[current_platform_type],
                    'cargos': current_cargos.copy()
                })
                current_cargos = []
            continue

        current_cargos.append({**cargo, 'x': total_cargos_length, 'y': 0, 'z': 0})

    if current_cargos:
        platforms.append({
            **types_platform[current_platform_type],
            'cargos': current_cargos.copy()
        })

    return platforms


def gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height):
    res = []
    for i in range(0, len(lst_cargo_height)):
        res.append(tuple((lst_cargo_len[i], lst_cargo_width[i], lst_cargo_height[i])))
    return res


def info_cargo(lst_cargo_weight, lst_cargo_len, lst_cargo_width, lst_cargo_height):
    res = []
    cargo_gab = gabarites(lst_cargo_len, lst_cargo_width, lst_cargo_height)
    for i in range(0, len(lst_cargo_len)):
        res.append(tuple((lst_cargo_weight[i], cargo_gab[i])))

    return res


def veight(cargo):
    return -cargo[0]


def square(cargo):
    print(cargo[1][0] * cargo[1][1])
    return (-cargo[1][0] * cargo[1][1])


if __name__ == '__main__':
    cargo = info_cargo(lst_cargo_weight, lst_cargo_len, lst_cargo_width, lst_cargo_height)
    import json

    print(json.dumps(select_platforms_by_cargos(cargos), indent=3))
    # my_lst.sort(key=square)
    # print(cargo)
    # print('-' * 20)
    # print(create_platforms_with_cargo(cargo))
