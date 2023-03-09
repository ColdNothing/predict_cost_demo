
#import required libraries
import os

#to create an application interface
import streamlit as st

#to work with arrays
import numpy as np

#for predicting cost with a model catboost
import catboost as cb
from catboost import CatBoostRegressor


#calculation of the cost of a basic house kit
#by CatBoost model
def predict_catboost(DATA, MODELS_PATH):

    #loading a working model

    model_cb = CatBoostRegressor()
    model_cb.load_model('Model_cb')

    #calculation of the cost of a house kit

    y_pred = model_cb.predict(DATA)

    return y_pred[0]

def result(DATA, MODELS_PATH):

    y_pred_out = predict_catboost(DATA, MODELS_PATH)
    y_pred_out = round(y_pred_out * 1000)

    st.write(' ')
    if y_pred_out % 10 == 1:
        st.write('Cтоимость базового домокомплекта: ', str(y_pred_out), ' рубль')
    elif (y_pred_out % 10) in [2, 3, 4]:
        st.write('Cтоимость базового домокомплекта: ', str(y_pred_out), ' рубля')
    else:
        st.write('Cтоимость базового домокомплекта: ', str(y_pred_out), ' рублей')

    return


#displaying a descriptive block based on user-entered data
def information_block_output (length, width, double_bar_per, attic_type, floor_area, veranda_area,
                              num_of_rooms, ground_floor_height, roof_type, roof_slope_angle, windows_area):

    st.write('')
    st.write(house_type, ' размером ', str(round(length, 2)), 'x', str(round(width, 2)), ' м')
    if double_bar_per == 0:
        st.write('из одинарного бруса')
    else:
        st.write('с процентовкой двойного бруса ', str(double_bar_per))
    st.write('Мансарда', attic_type.lower())
    st.write('Площадь жилой зоны приблизительно ', str(floor_area), 'м.кв')
    if veranda_area == 0:
        st.write('Без дополнительных элементов (террасы/веранды/крыльца)')
    else:
        st.write('Площадь веранды/террасы/крыльца приблизительно: ', str(veranda_area), 'м.кв')
    st.write('Количество помещений: ', str(num_of_rooms))
    st.write('Высота первого этажа: ', str(ground_floor_height), ' м')
    st.write('Крыша', roof_type.lower(), ', угол скатов крыши ', roof_slope_angle.lower())
    st.write('Площадь оконных проёмов приблизительно ', str(windows_area), ' м.кв')

    return


# formation of input vector to be fed
# into the prediction CatBoost model

def make_data_for_CB (house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area,
                      ground_floor_height, num_of_rooms, double_bar_per, windows_area):

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

    data = np.expand_dims(data, axis = 0)

    return data

#receiving and pre-processing data from the user
def input_transform_data():

    #drawing the user interface
    house_type = st.radio('Тип строения', ['Дом', 'Баня', 'Беседка'],
                          help='Для дома считаются черновый полы и потолки, для бани и веранды - чистовые')
    attic_type = st.radio('Тип мансарды', ['Нет мансарды', 'Поднятая', 'Неподнятая'],
                          help='У поднятой мансарды высота боковых стен 1,56 метра')
    double_bar_per = st.number_input('Процент двойного бруса', min_value=0, max_value=100, value=60, step=5,
                                     help='Для одинарного бруса - 0, всё двойной брус - 100, все внешние стены двойные, все перегородки одинарные - 60')
    length = st.number_input('Длина в метрах', min_value=1.0, max_value=35.0, value=8.0, step=0.1,
                             help='По сторонам, на которые ложатся стропила и скаты крыши; вдоль обрешётки')
    width = st.number_input('Ширина в метрах', min_value=1.0, max_value=20.0, value=6.0, step=0.1,
                            help='По сторонам, на которых фронтоны, если они имеются')

    #double_bar_per default value calculation
    if double_bar_per == 0:
        floor_area_default = (length - 0.1) * (width - 0.1) - 0.5
    elif 65 >= double_bar_per >= 60:
        floor_area_default = (length - 0.5) * (width - 0.5) - 0.5
    elif 75 >= double_bar_per >= 70:
        floor_area_default = (length - 0.5) * (width - 0.5) - 1
    elif 85 >= double_bar_per >= 75:
        floor_area_default = (length - 0.5) * (width - 0.5) - 1.5
    elif 90 >= double_bar_per >= 85:
        floor_area_default = (length - 0.5) * (width - 0.5) - 2
    elif double_bar_per > 90:
        floor_area_default = (length - 0.5) * (width - 0.5) - 2.5
    else:
        area0 = (length - 0.1) * (width - 0.1) - 0.5
        area60 = (length - 0.5) * (width - 0.5) - 0.5
        k = double_bar_per / 60
        floor_area_default = area0 - (area0 - area60) * k

    # attic_type default value calculation
    if attic_type == 'Поднятая':
        floor_area_default = floor_area_default * 2
    elif attic_type == 'Неподнятая':
        floor_area_default = floor_area_default * 2.2

    floor_area_default = round(floor_area_default, 2)

    floor_area = st.number_input('Площадь полов жилой зоны', min_value=1.0, max_value=500.0, value=floor_area_default,
                                 step=1.0, help='по умолчанию рассчитывается автоматически')
    veranda_area = st.number_input('Площадь веранд, террас, крылец, балконов', min_value=0.0, max_value=120.0,
                                   value=0.0, step=1.0, help='всё, что не из профильного бруса, в сумме')
    ground_floor_height = st.number_input('Высота первого этажа в метрах ', min_value=1.0, max_value=4.0, value=2.57,
                                          step=0.1, help='задавать чуть больше. например, 2,57 для 2,5')
    num_of_rooms = st.number_input('Количество помещений', min_value=1, max_value=35, value=6, step=1,
                                   help='все, которые огорожены перегородками, в том числе холлы, коридоры итп')
    roof_type = st.radio('Тип крыши', ['Двускатная', 'Односкатная', 'Вальмовая', 'Сложная'])
    roof_slope_angle = st.radio('Величина угла крыши', ['Маленький', 'Средний', 'Большой'],
                                help='Маленький - меньше 20 градусов, Средний от 20 до 35 градусов, Большой - больше 35 градусов')
    windows_area = st.number_input('Площадь оконных проёмов', min_value=0.0, max_value=90.0, value=14.0, step=0.5,
                                   help='предварительно можно брать 2 м.кв на одно окно, кроме совсем маленьких')

    if attic_type == 'Нет мансарды':
        attic_type = 'Отсутствует'

    start = st.button('ПОСЧИТАТЬ')

    return start, house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area, \
           ground_floor_height, num_of_rooms, double_bar_per, windows_area



#main script

#paths to folders with working data of models
working_path = os.getcwd()

#path to working models
models_path = working_path



#application header display
st.markdown('# CЕЙЧАС ВСЁ ПОСЧИТАЕМ!')
st.markdown('## Расчёт стоимости базового домокомплекта')

st.markdown('### Введите следующие данные')


#user input
start, house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, \
veranda_area, ground_floor_height, num_of_rooms, double_bar_per, windows_area = input_transform_data()



#formation of input vector to be fed
#into the prediction CatBoost model
data = make_data_for_CB(house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area,
                        ground_floor_height, num_of_rooms, double_bar_per, windows_area)



#by pressing the сalculate button
if start:

    #displaying a descriptive block based on user-entered data
    information_block_output (length, width, double_bar_per, attic_type, floor_area, veranda_area,
                              num_of_rooms, ground_floor_height, roof_type, roof_slope_angle, windows_area)

    # prediction of the cost of a basic house kit
    # as the average prediction of the two best neural network models
    # and CatBoost models
    result(data, models_path)
