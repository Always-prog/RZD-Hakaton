import pandas as pd
import functions_for_boxes as bx
import random
random.seed(1)

# Test_cargo_set
lst_cargo_weight = [6670, 4085, 395, 1865] * 5  # Веса грузов
lst_cargo_len = [3650, 3870, 1080, 4100] * 5  # Длинна грузов
lst_cargo_height = [1500, 1020, 390, 1865] * 5  # Высота грузов
lst_cargo_width = [3320, 2890, 1580, 1720] * 5  # Ширина грузов

cargos = [{'weight': lst_cargo_weight[i], 'length': lst_cargo_len[i], 'height': lst_cargo_height[i],
           'width': lst_cargo_width[i]} for i in range(len(lst_cargo_weight))]

materials = [
    "дерево",
    "сталь",
    "пакеты чушек свинца, цинка",
    "пакеты отливок алюминия",
    "железобетон",
    "вертикально устанавливаемые рулоны листовой стали",
    "пачки промасленной листовой стали"
]


def parse_cargos(data):
    # Создаем DataFrame из данных
    df = pd.DataFrame(data[1:], columns=data[0])

    # Преобразуем столбцы с количеством штук, весом и размерами в числовой формат
    df[['Кол-во (шт)', 'Длина (мм)', 'Ширина (мм)', 'Высота (мм)', 'Вес 1 ед (кг)']] = df[
        ['Кол-во (шт)', 'Длина (мм)', 'Ширина (мм)', 'Высота (мм)', 'Вес 1 ед (кг)']].apply(pd.to_numeric)

    # Создаем список грузов на основе данных в DataFrame
    cargo_list = []
    for _, row in df.iterrows():
        cargo = {
            'weight': row['Вес 1 ед (кг)'],
            'length': row['Длина (мм)'],
            'width': row['Ширина (мм)'],
            'height': row['Высота (мм)']
        }
        cargo_info = {
            'name': row['Наименование груза'],
            'packet_material': materials[int(row['Материал упаковки'])]
        }
        cargo_list.extend([cargo] * row['Кол-во (шт)'])
        for c in cargo_list:
            c.update(cargo_info)

    return cargo_list


def select_platforms_by_cargos(cargos):
    """
    Распределитель грузов по вагонам
    """
    random.shuffle(cargos)

    LIMIT_CARGOS_MASS = 50000  # 50 ТОНН.
    DEFAULT_PLATFORM = '13-401'

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
    current_platform_type = DEFAULT_PLATFORM
    current_cargos = []
    for cargo in filter(filter_unexpected, cargos):
        total_cargos_length = sum([c['length'] for c in current_cargos]) + (len(current_cargos) * bx.SPACE)
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
                current_platform_type = DEFAULT_PLATFORM
            continue

        current_cargos.append({**cargo, 'x': total_cargos_length, 'y': 0, 'z': 0})

    if current_cargos:
        platforms.append({
            **types_platform[current_platform_type],
            'cargos': current_cargos.copy()
        })

    # Сортируем тяжелые ящики к центру
    for n, platform in enumerate(platforms):
        platform_cargos = platform['cargos'].copy()
        # Сортируем грузы по весу в порядке убывания
        sorted_cargos = sorted(platform_cargos, key=lambda x: x['weight'])
        # Помещяем в центр самые тяжелые
        highest_in_middle = sorted_cargos[len(sorted_cargos) % 2::2] + sorted_cargos[::-2]

        # Список для хранения размещенных грузов с координатами
        placed_cargos = []

        x = 0
        for cargo in highest_in_middle:
            placed_cargos.append({
                **cargo,
                'x': x
            })
            x += bx.SPACE + cargo['length']

        platforms[n]['cargos'] = placed_cargos

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


def optimize_platforms(cargos):
    min_platforms = len(cargos)
    for i in range(500):
        platforms = len(select_platforms_by_cargos(cargos))
        random.shuffle(cargos)
        if platforms < min_platforms:
            min_platforms = platforms

        for i in range(500):
            random.shuffle(cargos)
            platforms = select_platforms_by_cargos(cargos)
            if len(platforms) == min_platforms:
                return platforms
        #Резервный вариант
        return platforms


if __name__ == '__main__':
    cargo = info_cargo(lst_cargo_weight, lst_cargo_len, lst_cargo_width, lst_cargo_height)
    import json

    # print([p['type'] for p in select_platforms_by_cargos(cargos)])
    #print(json.dumps(select_platforms_by_cargos(cargos), indent=3))
    # my_lst.sort(key=square)
    # print(cargo)
    print('-' * 20)
    print(len(optimize_platforms(cargos)))

