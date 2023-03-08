# Для работы с массивами
import numpy as np

# Для работы с датасетом
import pandas as pd


# Для работы с категориальными данными
from tensorflow.keras import utils

# Для создания полносвязной сети и модели
from tensorflow.keras.models import load_model


# Подключаем стандартизатор
from sklearn.preprocessing import StandardScaler

# Подключаем модуль считывания объекта из файла
import pickle

# Для градиентного бустинга
import catboost as cb
from catboost import CatBoostRegressor

#для работы с файловой системой
import os


# вывод предсказания стоимости базового домокомплекта

def value_output(y_pred_out):
    print('Стоимость базового домокомплекта: ', round(y_pred_out * 1000), ' рублей')


# предсказание стоимости базового домокомплекта

def predict_price(model, x_in, y_scaler):
    y_pred = model.predict(x_in, verbose=0)
    y_pred_unscaled = y_scaler.inverse_transform(y_pred).flatten()

    return y_pred_unscaled[0]


# вывод информации о рассчитываемом объекте

def out_info(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
         double_bar_per, roof_type, roof_slope_angle, windows_area):
    print()
    print()
    print('Тип здания: ', house_type)
    print('Длина здания: ', length)
    print('Ширина здания: ', width)
    print('Площадь пола жилой зоны: ', floor_area)
    print('Площадь веранды/террасы/балкона: ', veranda_area)
    print('Высота первого этажа: ', ground_floor_height)
    print('Тип мансарды: ', attic_type)
    print('Количество помещений: ', num_of_rooms)
    print('Процент двойного бруса: ', double_bar_per)
    print('Тип крыши: ', roof_type)
    print('Величина угла крыши: ', roof_slope_angle)
    print('Площадь оконных проёмов: ', windows_area)
    print()
    print()


# предсказание стоимости базового домокомплекта
# с помощью модели CatBoost
# и его вывод

def catboost_mode(house_type, length, width, floor_area, veranda_area,
              ground_floor_height, attic_type, num_of_rooms, double_bar_per,
              roof_type, roof_slope_angle, windows_area):

    Y_PRED_OUT = predict_catboost(house_type, length, width, floor_area,
                                  veranda_area, ground_floor_height, attic_type,
                                  num_of_rooms, double_bar_per, roof_type,
                                  roof_slope_angle, windows_area)

    out_info(house_type, length, width, floor_area, veranda_area,
             ground_floor_height, attic_type, num_of_rooms,
             double_bar_per, roof_type, roof_slope_angle, windows_area)

    value_output(Y_PRED_OUT)


# получение входных параметров

def get_input():
# Получаем входные данные для предсказания

    print()
    print('Введите необходимые данные для расчёта')
    print()

    house_type = input('Тип здания(Дом/Баня/Беседка): ')

    # дефолтный ввод категорий через Enter
    # ввод категорий с помощью цифр

    if house_type == '' or house_type == '1':
        house_type = 'Дом'
    if house_type == '2':
        house_type = 'Баня'
    if house_type == '3':
        house_type = 'Беседка'

    length = float(input('Длина здания: '))
    width = float(input('Ширина здания: '))
    floor_area = float(input('Площадь пола жилой зоны: '))
    veranda_area = float(input('Площадь веранды/террасы/балкона: '))
    ground_floor_height = float(input('Высота первого этажа: '))
    attic_type = input('Тип мансарды (Отсутствует/Неподнятая/Поднятая): ')

    # дефолтный ввод категорий через Enter
    # ввод категорий с помощью цифр

    if attic_type == '' or attic_type == '1':
        attic_type = 'Отсутствует'
    if attic_type == '2':
        attic_type = 'Неподнятая'
    if attic_type == '3':
        attic_type = 'Поднятая'

    num_of_rooms = int(input('Количество помещений: '))
    double_bar_per = int(input('Процент двойного бруса: '))
    roof_type = input('Тип крыши(Двускатная/Односкатная/Вальмовая/Сложная):  ')

    # дефолтный ввод категорий через Enter
    # ввод категорий с помощью цифр

    if roof_type == '' or roof_type == '1':
        roof_type = 'Двускатная'
    if roof_type == '2':
        roof_type = 'Односкатная'
    if roof_type == '3':
        roof_type = 'Вальмовая'
    if roof_type == '4':
        roof_type = 'Сложная'

    roof_slope_angle = input('Величина угла крыши(Маленький/Средний/Большой): ')

    # дефолтный ввод категорий через Enter
    # ввод категорий с помощью цифр

    if roof_slope_angle == '' or roof_slope_angle == '2':
        roof_slope_angle = 'Средний'
    if roof_slope_angle == '1':
        roof_slope_angle = 'Маленький'
    if roof_slope_angle == '3':
        roof_slope_angle = 'Большой'

    windows_area = float(input('Площадь оконных проёмов: '))

    return house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms, double_bar_per, roof_type, roof_slope_angle, windows_area


# обработка входных данных
# нормирование числовых
# и привидение категориальных в формат OHE

def data_transorm(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
              double_bar_per, roof_type, roof_slope_angle, windows_area):
# Преобразуем категориальные данные в массив OHE

    OneHot = []

    house_type_cat = ['Баня', 'Беседка', 'Дом']
    attic_type_cat = ['Неподнятая', 'Отсутствует', 'Поднятая']
    roof_type_cat = ['Вальмовая', 'Двускатная', 'Односкатная', 'Сложная']
    roof_slope_angle_cat = ['Большой', 'Маленький', 'Средний']

    house_type_OHE = utils.to_categorical(np.array(house_type_cat.index(house_type)), num_classes=len(house_type_cat))
    OneHot.append(house_type_OHE)

    attic_type_OHE = utils.to_categorical(np.array(attic_type_cat.index(attic_type)), num_classes=len(attic_type_cat))
    OneHot.append(attic_type_OHE)

    roof_type_OHE = utils.to_categorical(np.array(roof_type_cat.index(roof_type)), num_classes=len(roof_type_cat))
    OneHot.append(roof_type_OHE)

    roof_slope_angle_OHE = utils.to_categorical(np.array(roof_slope_angle_cat.index(roof_slope_angle)),
                                                num_classes=len(roof_slope_angle_cat))
    OneHot.append(roof_slope_angle_OHE)

    # Объединяем все массивы в один
    OneHotArray = np.concatenate([i for i in OneHot], dtype=object)

    # Нормируем входные числовые данные

    scaler_path = os.path.join (working_path, 'parameters')

    with open(os.path.join(scaler_path, 'length_scaler.pkl'), 'rb') as fp:
        length_scaler = pickle.load(fp)

    length_scaled = length_scaler.transform(np.array(length).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path,'width_scaler.pkl'), 'rb') as fp:
        width_scaler = pickle.load(fp)

    width_scaled = width_scaler.transform(np.array(width).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'floor_area_scaler.pkl'), 'rb') as fp:
        floor_area_scaler = pickle.load(fp)

    floor_area_scaled = floor_area_scaler.transform(np.array(floor_area).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'veranda_area_scaler.pkl'), 'rb') as fp:
        veranda_area_scaler = pickle.load(fp)

    veranda_area_scaled = veranda_area_scaler.transform(np.array(veranda_area).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'ground_floor_height_scaler.pkl'), 'rb') as fp:
        ground_floor_height_scaler = pickle.load(fp)

    ground_floor_height_scaled = ground_floor_height_scaler.transform(
        np.array(ground_floor_height).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'num_of_rooms_scaler.pkl'), 'rb') as fp:
        num_of_rooms_scaler = pickle.load(fp)

    num_of_rooms_scaled = num_of_rooms_scaler.transform(np.array(num_of_rooms).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'double_bar_per_scaler.pkl'), 'rb') as fp:
        double_bar_per_scaler = pickle.load(fp)

    double_bar_per_scaled = double_bar_per_scaler.transform(np.array(double_bar_per).reshape(-1, 1)).flatten()

    with open(os.path.join(scaler_path, 'windows_area_scaler.pkl'), 'rb') as fp:
        windows_area_scaler = pickle.load(fp)

    windows_area_scaled = windows_area_scaler.transform(np.array(windows_area).reshape(-1, 1)).flatten()

    # формирование входного вектора данных для подачи в НС

    x_in = OneHotArray
    x_in = np.append(x_in, length_scaled)
    x_in = np.append(x_in, width_scaled)
    x_in = np.append(x_in, floor_area_scaled)
    x_in = np.append(x_in, veranda_area_scaled)
    x_in = np.append(x_in, ground_floor_height_scaled)
    x_in = np.append(x_in, num_of_rooms_scaled)
    x_in = np.append(x_in, double_bar_per_scaled)
    x_in = np.append(x_in, windows_area_scaled)

    x_in = np.array(x_in, dtype=np.float64)

    x_in = np.expand_dims(x_in, axis=0)

    return x_in


# обработка входных данных
# и вывод предсказанной стоимости домокомплекта

def tranform_predict_output(MODEL, Y_SCALER, house_type, length, width, floor_area, veranda_area, ground_floor_height,
                        attic_type, num_of_rooms, double_bar_per, roof_type, roof_slope_angle, windows_area):
    # обработка входных данных
    # нормирование числовых
    # и привидение категориальных в формат OHE
    X_IN = data_transorm(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type,
                         num_of_rooms, double_bar_per, roof_type, roof_slope_angle, windows_area)

    # предсказание стоимости базового домокомплекта
    Y_PRED_OUT = predict_price(MODEL, X_IN, Y_SCALER)

    # вывод информации о рассчитываемом объекте
    out_info(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
             double_bar_per, roof_type, roof_slope_angle, windows_area)

    # вывод предсказания стоимости базового домокомплекта
    value_output(Y_PRED_OUT)

    return


# предсказание и вывод стоимости домокомплекта
# без вывода информации о рассчитываемом объекте

def predict_output(MODEL, X_IN, Y_SCALER):
    # предсказание стоимости базового домокомплекта
    Y_PRED_OUT = predict_price(MODEL, X_IN, Y_SCALER)

    # вывод предсказания стоимости базового домокомплекта
    value_output(Y_PRED_OUT)

    return


# предсказание и вывод стоимости домокомплекта
# с помощью модели CatBoost

def predict_catboost(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
                 double_bar_per, roof_type, roof_slope_angle, windows_area):
    data = []
    data.append(house_type)
    data.append(length)
    data.append(width)
    data.append(floor_area)
    data.append(veranda_area)
    data.append(ground_floor_height)
    data.append(attic_type)
    data.append(num_of_rooms)
    data.append(double_bar_per)
    data.append(roof_type)
    data.append(roof_slope_angle)
    data.append(windows_area)

    data = np.array(data)

    data = np.expand_dims(data, axis=0)

    col_names = ['House type', 'Length', 'Width', 'Floor area',
                 'Veranda area', 'Ground floor height', 'Attic type', 'Number of rooms',
                 'Double bar percentage', 'Roof type', 'Roof slope angle',
                 'Area of window openings']

    input_data = pd.DataFrame(data=data, columns=col_names)



    # загрузка рабочей модели

    model_cb = CatBoostRegressor()

    model_path = os.path.join (os.getcwd(), 'models')
    model_cb.load_model(os.path.join (model_path, 'Model_cb'))

    y_pred = model_cb.predict(input_data)

    return y_pred[0]


# пути к разным рабочим моделям
# загрузка рабочей модели

#paths to folders with working data of models
working_path = os.getcwd()

#path to working models
models_path = os.path.join (working_path, 'models')

models_list = ['Model_1_13.h5', 'Model_1_1.h5', 'Model_1_7.h5', 'Model_1_8.h5', 'Model_1_17.h5']

num_models = len(models_list)

i = 0
MODEL = load_model(os.path.join(models_path, models_list[i]))

# нормирование целевого параметра
# стоимости базового домокомплекта
#path to data normalization parameters
scaler_path = os.path.join (working_path, 'parameters')

with open(os.path.join (scaler_path, 'y_scaler.pkl'), 'rb') as fp:
    Y_SCALER = pickle.load(fp)

# предсказать с помощью модели CatBoost
print()
mode = input('Предсказать моделью CatBoost? да/нет ')
print()

# получение входных данные для предсказания
house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms, double_bar_per, roof_type, roof_slope_angle, windows_area = get_input()

# обработка входных данных
# нормирование числовых
# и привидение категориальных в формат OHE
X_IN = data_transorm(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
                 double_bar_per, roof_type, roof_slope_angle, windows_area)

if mode == 'да':

    catboost_mode(house_type, length, width, floor_area, veranda_area,
                  ground_floor_height, attic_type, num_of_rooms, double_bar_per,
                  roof_type, roof_slope_angle, windows_area)
else:

    # предсказание стоимости базового домокомплекта
    Y_PRED_OUT = predict_price(MODEL, X_IN, Y_SCALER)

    # вывод информации о рассчитываемом объекте
    out_info(house_type, length, width, floor_area, veranda_area, ground_floor_height, attic_type, num_of_rooms,
             double_bar_per, roof_type, roof_slope_angle, windows_area)

    # вывод предсказания стоимости базового домокомплекта
    value_output(Y_PRED_OUT)

while True:

    print()
    ans = input('Изменить какой-нибудь параметр? да/нет ')
    print()

    if ans == 'нет':
        break

    elif ans == 'да':

        print()
        print('Какой параметр хотите изменить? ')
        print('Введите шифр \n')

        print('Тип здания - тз,  Длина здания - дл,  Ширина здания - шр,  Площадь пола жилой зоны - плп, ')
        print('Площадь веранды/террасы/балкона - плв,  Высота первого этажа - в1, ')
        print('Тип мансарды - тм,  Количество помещений - кп,  Процент двойного бруса - пдб, ')
        print('Тип крыши - тк,  Величина угла крыши - ук,  Площадь оконных проёмов - по ')
        print('Другая модель нейросети - нс, Предсказание моделью CatBoost - св')
        print('Усреднённое предсказание пяти лучших моделей нейросетей - 5нс')
        print('Усреднённое предсказание двух лучших моделей нейросетей и модели CatBoost - св+нс')
        print()

        select = input()
        print()

        if select == 'тз':
            house_type = input('Тип здания(Дом/Баня/Беседка): ')
        elif select == 'дл':
            length = float(input('Длина здания: '))
        elif select == 'шр':
            width = float(input('Ширина здания: '))
        elif select == 'плп':
            floor_area = float(input('Площадь пола: '))
        elif select == 'плв':
            veranda_area = float(input('Площадь веранды/террасы/балкона: '))
        elif select == 'в1':
            ground_floor_height = float(input('Высота первого этажа: '))
        elif select == 'тм':
            attic_type = input('Тип мансарды (Отсутствует/Неподнятая/Поднятая): ')
        elif select == 'кп':
            num_of_rooms = int(input('Количество помещений: '))
        elif select == 'пдб':
            double_bar_per = int(input('Процент двойного бруса: '))
        elif select == 'тк':
            roof_type = input('Тип крыши(Двускатная/Односкатная/Вальмовая/Сложная):  ')
        elif select == 'ук':
            roof_slope_angle = input('Величина угла крыши(Маленький/Средний/Большой): ')
        elif select == 'по':
            windows_area = float(input('Площадь оконных проёмов: '))

        if select in ['тз', 'дл', 'шр', 'плп', 'плв', 'в1', 'тм', 'кп', 'пдб', 'тк', 'ук', 'по']:
            tranform_predict_output(MODEL, Y_SCALER, house_type, length, width,
                                    floor_area, veranda_area, ground_floor_height,
                                    attic_type, num_of_rooms, double_bar_per,
                                    roof_type, roof_slope_angle, windows_area)

        elif select == 'нс':
            out_info(house_type, length, width, floor_area, veranda_area,
                     ground_floor_height, attic_type, num_of_rooms,
                     double_bar_per, roof_type, roof_slope_angle, windows_area)
            for i in range(num_models):
                MODEL = load_model(os.path.join(models_path, models_list[i]))
                predict_output(MODEL, X_IN, Y_SCALER)

        elif select == '5нс':
            out_info(house_type, length, width, floor_area, veranda_area,
                     ground_floor_height, attic_type, num_of_rooms,
                     double_bar_per, roof_type, roof_slope_angle, windows_area)
            Y_PRED_OUT = 0
            for i in range(num_models):
                MODEL = load_model(os.path.join(models_path, models_list[i]))
                Y_PRED_OUT += predict_price(MODEL, X_IN, Y_SCALER)
            Y_PRED_OUT = Y_PRED_OUT / num_models
            value_output(Y_PRED_OUT)

        elif select == 'св':
            catboost_mode(house_type, length, width, floor_area, veranda_area,
                          ground_floor_height, attic_type, num_of_rooms,
                          double_bar_per, roof_type, roof_slope_angle, windows_area)

        elif select == 'св+нс':
            Y_PRED_OUT = predict_catboost(house_type, length, width, floor_area,
                                          veranda_area, ground_floor_height,
                                          attic_type, num_of_rooms, double_bar_per,
                                          roof_type, roof_slope_angle, windows_area)
            for i in range(2):
                MODEL = load_model(os.path.join(models_path, models_list[i]))
                Y_PRED_OUT += predict_price(MODEL, X_IN, Y_SCALER)
            Y_PRED_OUT = Y_PRED_OUT / 3
            out_info(house_type, length, width, floor_area, veranda_area,
                     ground_floor_height, attic_type, num_of_rooms,
                     double_bar_per, roof_type, roof_slope_angle, windows_area)
            value_output(Y_PRED_OUT)


        else:
            print('Нет такого шифра \n')
            print('Повторите ввод \n')

