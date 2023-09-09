"""
TODO:
ПРОВЕРИТЬ КОРРЕКТНОСТЬ НА ЗНАЧЕНИЯХ ИЗ ФАЙЛА!!!

ВСЕ ЗНАЧЕНИЯ В ФУНКЦИИ ДОЛЖНЫ ПЕРЕДАВАТЬСЯ В РАМКАХ
ОДНОГО ВАГОНА, ЕСЛИ НЕ УКАЗАНО ИНОЕ

Предполагаемый формат входных данных - списки значений грузов в рамках одной платформы.
lst_cargo_veight - список весов всех грузов
carriage_len - длинна вагона, для которого производится расчёт
lst_cargo_len - список длин грузов

ПРОВЕРИЛИ = False
"""

#Тестовый набор значений. Допустим, имеется 4 груза.
lst_cargo_veight = [6670, 4085, 395, 1865]
lst_cargo_len = [3650, 3870, 1080, 4100]
lst_cargo_height = [1500, 1020, 390, 1865]
lst_cargo_width = [3320, 2890, 1580, 1720]

lst_cargo_material = []

#Дистанция между грузами в миллиметрах
SPACE = 150

#Название платформы : грузоподъёмность, длинна и ширина,  вес вагона(тонны), высота центра тяжести вагона,
#площадь стороны, площадь платформы(верха)
#
#РАСШИРИТЬ НА ТЯЖЕЛЫЕ ПЛАТФОРМЫ И АДАПТИРОВАТЬ КОД
types_platform = {"13-401" : (70, (13400, 2770), 20.92, 1810, 36841000),
                  "13-926" : (73, (18400, 2830),27, 1807, 51789000)}

def main():
    pass


def summator_delta_centermass():
    """
    Должна возвращать суммарное отклонение центра масс.
    Вычисляется для единичного груза.
    """
    pass


def gravity_offset(carriage_len,cargo_len,lst_cargo_veight): #FIXME
    """Смещение ЦТ грузов в вагоне
    cargo_len is i lst_cargo_len -> lst_cargo_len[i]"""
    center_mass = lst_cargo_len / 2 #FIXME
    delta_center_mass = (0.5 * (carriage_len))
    delta_center_mass -= summator_delta_centermass() / sum(lst_cargo_veight)

    return delta_center_mass


def gravity_height(lst_cargo_height, lst_cargo_weight):
    """Общая высота ЦТ грузов в вагоне"""
    res_1 = 0
    for i in range(0,len(lst_cargo_height)-1):
        res_1 += lst_cargo_height[i] * 0.5 * (lst_cargo_weight[i]/1000)
    res_1 = res_1 / (sum(lst_cargo_weight)/1000)
    return res_1


def cargo_stability(cargo_height:list, lst_cargo_veight:list, types_platform, type:str):
    """Общая высота ценра тяжести вагона. type - выбранная платформа."""
    #ПЕРЕДЕЛАТЬ СОГЛАСНО НОВЫМ ВХОДНЫМ ДАННЫМ
    res_1 = 0
    platform = types_platform(type)
    res_1 += gravity_height(cargo_height, lst_cargo_veight) + (platform(2) * platform(3))
    res_1 = res_1 / (sum(lst_cargo_veight) + platform(2))
    if res_1 < 2300:
        return res_1
    else:
        print("Центр тяжести слишком высоко.")
        return False


def windward_surface(lst_cargo):
    """Расчёт наветренной поверхности. Пункт 3.2"""
    pass


def func_4_1(type_hard:bool, lst_cargo_veight:list):
    """type_hard = True, если крепление жёсткое, и False в противном случае.
    Продольная инерционная сила"""
    res = 0
    my_res = []

    if type_hard:
        a_22 = 1.9
        a_94 = 1.67
    else:
        a_22 = 1.2
        a_94 = 0.97

    veight = sum(lst_cargo_veight) / 1000
    res = a_22 - ((veight * (a_22 - a_94)) / 72)

    for cargo in lst_cargo_veight:
        my_res.append(res*(cargo / 1000))
        print(res*(cargo / 1000))

    return my_res


def func_4_2(carriage_len:int): #FIXME
    """Поперечная инерционная сила"""
    pass


def func_4_5(lst_cargo_veight,lst_cargo_material):
    pass



if __name__ == '__main__':
    print(sum(lst_cargo_veight))
    print(func_4_1(False,lst_cargo_veight)) #Подсчёт продольной инерции для каждого груза

    print(gravity_height(lst_cargo_height, lst_cargo_veight))