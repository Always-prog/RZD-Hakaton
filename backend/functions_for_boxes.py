"""
TODO:
ПРОВЕРИТЬ КОРРЕКТНОСТЬ НА ЗНАЧЕНИЯХ ИЗ ФАЙЛА!!!

ВСЕ ЗНАЧЕНИЯ В ФУНКЦИИ ДОЛЖНЫ ПЕРЕДАВАТЬСЯ В РАМКАХ
ОДНОГО ВАГОНА, ЕСЛИ НЕ УКАЗАНО ИНОЕ

ПРОВЕРИЛИ = False
"""
#Дистанция между грузами
SPACE = 0

#Название платформы : грузоподъёмность, длинна, вес вагона, высота центра тяжести вагона
#РАСШИРИТЬ НА ТЯЖЕЛЫЕ ПЛАТФОРМЫ И АДАПТИРОВАТЬ КОД
types_platform = {"13-401" : (70, 13400, 20.92, 1810), "13-Н451" : (63, 13400, 21.3, 1810),
                  "13-926" : (73, 18400, 27, 1807)}

def main():
    pass


def choice_platform(types_platform, cargo):
    """
    Выбирает платформу в зависимости от груза
    """
    pass
    return platform, lst_cargo


def cargo_input():
    a = int(input("Введите массу груза: "))
    b = int(input("Введите "))


def summator_mass(lst_cargo:dict):
    """
    Подсчёт массы всех грузов
    """
    res_1 = 0
    for i, j in lst_cargo.items():
        res_1 += i * j
    return res_1


def summator_delta_centermass():
    """
    Должна возвращать суммарное отклонение центра масс
    """
    pass


def gravity_offset(carriage_len,cargo_len,lst_cargo,CHANGE_ME=1):
    """Смещение ЦТ грузов в вагоне"""
    center_mass = cargo_len / 2
    delta_center_mass = (0.5 * (carriage_len))
    delta_center_mass -= summator_delta_centermass() / summator_mass(lst_cargo.items()(0))

    return delta_center_mass


def gravity_height(cargo_height:list, cargo_veight:list, lst_cargo):
    """Общая высота ЦТ"""
    res_1 = 0
    for i in range(0,len(cargo_height)-1):
        res_1 += cargo_height * 0.5 * cargo_veight
    res_1 = res_1 / summator_mass(lst_cargo.items()(0))
    return res_1


def cargo_stability(cargo_height:list, cargo_veight:list, types_platform):




if __name__ == '__main__':
    print(summator_mass({100:1,140:3}))