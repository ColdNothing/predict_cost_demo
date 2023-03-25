
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
#and volume of wall kit
#by CatBoost models

def predict_catboost(DATA, MODELS_PATH):

    #loading a working models
    #for predict cost of basic house kit
    #and volume of wall kit

    model_bdk = CatBoostRegressor()
    model_sk = CatBoostRegressor()

    model_bdk.load_model('Model_cb_bdk')
    model_sk.load_model('Model_cb_sk')

    #calculation of the cost of a house kit
    #and volume of wall kit

    cost_bdk = model_bdk.predict(DATA)
    volume_sk = model_sk.predict(DATA)

    return cost_bdk[0], volume_sk[0]


#display of calculated costs and volumes

def result_out(phrase, cost_bdk_out, volume_bdk_out, cost_sk_out, volume_sk_out):

    st.write(' ')
    if cost_bdk_out % 10 == 1:
        st.write(phrase[0], str(cost_bdk_out), ' рубль')
    elif (cost_bdk_out % 10) in [2, 3, 4]:
        st.write(phrase[0], str(cost_bdk_out), ' рубля')
    else:
        st.write(phrase[0], str(cost_bdk_out), ' рублей')
    st.write(phrase[1], str(volume_bdk_out), ' м.куб.')

    if cost_sk_out % 10 == 1:
        st.write(phrase[2], str(cost_sk_out), ' рубль')
    elif (cost_sk_out % 10) in [2, 3, 4]:
        st.write(phrase[2], str(cost_sk_out), ' рубля')
    else:
        st.write(phrase[2], str(cost_sk_out), ' рублей')
    st.write(phrase[3], str(volume_sk_out), ' м.куб.')

    return


# additional calculations costs and volumes before display it

def result(DATA, MODELS_PATH, slab_foundation, first_floor_area, house_mode, floor_seiling, floor_area,
           roof_type, roof_slope_angle, attic_type):


    cost_bdk_out, volume_sk_out = predict_catboost(DATA, MODELS_PATH)

    #price of 1 cubic meter of wall material
    price_wall_vl = 57000

    #average price per cube of the rest of the material
    price_rest_vl = 35000

    #average price per cube of finishing floor
    price_finishing_floor_vl = 48500

    #average price per square strapping and ground floor for houses (with draft floor)
    price_strapping_sq_1 = 1700

    #average price per square strapping and ground floor for baths (with finishing floor)
    price_strapping_sq_0 = 2855

    #price per volume strapping and ground floor for houses (with draft floor)
    price_strapping_vl = 25600
    price_draft_floor_vl = 25600

    #price per square finishing floor
    price_finish_floor_sq = 2168

    #average price stapping per 1 square of floor area
    price_strapping_sq = price_strapping_sq_0 - price_finish_floor_sq

    #calculation cost of basic house kit,
    #volume of wall material,
    #cost of wall kit
    #and volume of basic house kit

    cost_bdk_out = round(cost_bdk_out * 1000)
    volume_sk_out = round(volume_sk_out, 2)
    cost_sk_out = round(volume_sk_out * price_wall_vl)
    volume_bdk_out = round(((cost_bdk_out - cost_sk_out) / price_rest_vl + volume_sk_out), 2)


    #some output phrases
    phr1 = 'Предварительная стоимость базового домокомплекта: '
    phr2 = 'Предварительная стоимость стенокомплекта: '
    phr3 = 'Предварительная стоимость домокомплекта на фундаментную плиту'
    phr4 = 'Предварительная стоимость домокомплекта с '
    phr5 = 'Вероятный объём базового домокомплекта: '
    phr6 = 'Вероятный объём стенокомплекта: '
    phr7 = 'Вероятный объём домокомплекта на фундаментную плиту: '
    phr8 = 'Вероятный объём домокомплекта с '

    phrase = []
    phrase[0] = phr1
    phrase[1] = phr5
    phrase[2] = phr2
    phrase[3] = phr6


    #cost and volume of basic house kit for slab foundation

    if slab_foundation:
        if house_mode:
            cost_bdk_out = round (cost_bdk_out - first_floor_area * price_strapping_sq_1)
            volume_bdk_out = round((volume_bdk_out - (first_floor_area * price_strapping_sq_1) / price_strapping_vl), 2)
        else:
            cost_bdk_out = round (cost_bdk_out - first_floor_area * price_strapping_sq_0)
            volume_strapping_floor = (price_strapping_sq / price_strapping_vl) + (price_finish_floor_sq / price_finishing_floor_vl)
            volume_bdk_out = round((volume_bdk_out - volume_strapping_floor), 2)


    if (house_mode and (floor_seiling != 'Черновые'))  or (not house_mode and (floor_seiling != 'Чистовые')):



        #for not default floor and seiling

        #diff_fs - cost difference between the finished and rough floor and ceiling
        #1,04 - coefficient taking into account floors in doorways
        #1,07 - coefficient taking into account the area of the spikes of the finished floor and ceiling
        #0,03 - draft floor and ceiling thickness
        #0,04 - finishing floor thickness
        #0,025 - finishing ceiling thickness
        #coef_angle - coefficient of increase in the ceiling area of attic (1-1.3)

        coef_angle = 1

        if attic_type in ['Нет мансарды', 'Отсутствует'] or roof_type == 'Вальмовая':
            coef_angle = 1
        elif roof_type == 'Cложная':
            coef_angle = 1,3
        elif roof_type == 'Двускатная':
            if roof_slope_angle == 'Большой':
                coef_angle = 1.3
            elif roof_slope_angle == 'Средний':
                    coef_angle = 1.2
            elif roof_slope_angle == 'Маленький':
                coef_angle = 1.1
        elif roof_type == 'Односкатная':
            if roof_slope_angle == 'Большой':
                coef_angle = 1.25
            elif roof_slope_angle == 'Средний':
                    coef_angle = 1.2
            elif roof_slope_angle == 'Маленький':
                    coef_angle = 1.1


        price_finish_ceiling_vl = 52500
        price_draft_ceiling_vl = 25600


        price_draft_floor_sq = price_draft_floor_vl * 1.04 * 0.03
        price_finish_floor_sq = price_finishing_floor_vl * 1.04 * 0.04 * 1.07
        price_draft_seiling_sq = price_draft_ceiling_vl * 0.03 * coef_angle
        price_finish_floor_sq = price_draft_ceiling_vl * 0.025 * 1.07 * coef_angle

        diff_floor = price_finish_floor_sq - price_draft_floor_sq
        diff_ceiling = price_finish_floor_sq - price_draft_seiling_sq

        #attic area. = 0 if no attic
        attic_area = floor_area - first_floor_area

        if house_mode:
            if floor_seiling == 'Чистовые':
                if not slab_foundation:
                    diff_fs = diff_floor + diff_ceiling
                    cost_bdk_out = round(cost_bdk_out + floor_area * diff_fs)
                else:
                    cost_bdk_out = round(cost_bdk_out + floor_area * diff_ceiling + attic_area * diff_floor)
            elif floor_seiling == 'Чистовой пол и черновой потолок':
                if not slab_foundation:
                    cost_bdk_out = round(cost_bdk_out + floor_area * diff_floor)
                else:
                    cost_bdk_out = round(cost_bdk_out + attic_area * diff_floor)
            elif floor_seiling == 'Чистовой потолок и черновой пол':
                cost_bdk_out = round(cost_bdk_out + floor_area * diff_seling)

        if not house_mode:
            if floor_seiling == 'Черновые':
                if not slab_foundation:
                   diff_fs = diff_floor + diff_ceiling
                   cost_bdk_out = round(cost_bdk_out - floor_area * diff_fs)
                else:
                   cost_bdk_out = round(cost_bdk_out - floor_area * diff_ceiling - attic_area * diff_floor)
            elif floor_seiling == 'Чистовой пол и черновой потолок':
                if not slab_foundation:
                   cost_bdk_out = round(cost_bdk_out - floor_area * diff_floor)
                else:
                   cost_bdk_out = round(cost_bdk_out - attic_area * diff_floor)
            elif floor_seiling == 'Чистовой потолок и черновой пол':
               cost_bdk_out = round(cost_bdk_out - floor_area * diff_seling)


    result_out(phrase, cost_bdk_out, volume_bdk_out, cost_sk_out, volume_sk_out)

    return


#displaying a descriptive block based on user-entered data
def information_block_output (house_type, length, width, double_bar_per, attic_type, floor_area, veranda_area,
                              num_of_rooms, ground_floor_height, roof_type, roof_slope_angle, windows_area, floor_ceiling
                              ):

    if (house_type == 'Дом') and (double_bar_per == 0):
        house_type = 'Летний домик'

    st.write('')
    st.write(house_type, ' размером ', str(round(length, 2)), 'x', str(round(width, 2)), ' м')
    if (house_type == 'Баня') and (double_bar_per == 0):
        st.write('из одинарного бруса')
    if double_bar_per == 100:
        st.write('полностью из двойного бруса')
    elif double_bar_per == 60:
        st.write('cо внешними стенами из двойного бруса, все внутренние перегородки из одинарного бруса')
    elif double_bar_per in [65,70]:
        st.write('со внешними стенами из двойного бруса, почти все внутренние перегородки из одинарного бруса')
    elif double_bar_per == 75:
        st.write('со внешними стенами из двойного бруса, внутренние перегородки частично из двойного бруса')
    elif double_bar_per in [80,85]:
        st.write('со внешними стенами из двойного бруса, большая часть внутренних перегородок из двойного бруса')
    elif double_bar_per in [90,95]:
        st.write('со внешними стенами из двойного бруса, почти все внутренние перегородки из двойного бруса')
    elif (double_bar_per > 0) and (double_bar_per < 50):
        st.write('почти все стены и перегородки в нём(ней) из одинарного бруса')
    else:
        st.write('со стенами и перегородками большей частью из двойного бруса')
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
    if floor_ceiling == 'Черновые':
        st.write('Пол и потолок черновые')
    elif floor_ceiling == 'Чистовые':
        st.write('Пол и потолок чистовые')
    else:
        st.write(floor_ceiling)

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
                          help='По умолчанию для домов считаются черновый полы и потолки, для бань и беседок - чистовые')

    attic_type = st.radio('Тип мансарды', ['Нет мансарды', 'Поднятая', 'Неподнятая'],
                            help='У поднятой мансарды высота боковых стен 1,56 метра')
    double_bar_per = st.slider('Процент двойного бруса', min_value=0, max_value=100, value=60, step=5,
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

    import copy
    first_floor_area = copy.copy(floor_area_default)

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

    roof_slope_angle = st.radio('Величина угла крыши', ['Средний', 'Маленький', 'Большой'],
                                help='Маленький - меньше 20 градусов, Средний от 20 до 35 градусов, Большой - больше 35 градусов')
    windows_area = st.number_input('Площадь оконных проёмов', min_value=0.0, max_value=90.0, value=14.0, step=0.5,
                                   help='предварительно можно брать 2 м.кв на одно окно, кроме совсем маленьких')

    if attic_type == 'Нет мансарды':
        attic_type = 'Отсутствует'

    #floors and ceilings (draft or finishin)
    if house_type == 'Дом':
        floor_ceiling = st.selectbox('Пол и потолок', ['Черновые', 'Чистовые', 'Чистовой пол и черновой потолок', 'Чистовой потолок и черновой пол'],
                                      help='По умолчанию потолки и полы считаются черновыми', label_visibility="visible")
    else:
        floor_ceiling = st.selectbox('Пол и потолок', ['Чистовые', 'Чистовой пол и черновой потолок', 'Чистовой потолок и черновой пол', 'Черновые'],
                                      help='По умолчанию потолки и полы считаются чистовыми', label_visibility="visible")


    slab_foundation = st.checkbox('Плитный фундамент', value=False, help='Расчёт стоимостей под фундаментную плиту',
                                  label_visibility="visible")

    start = st.button('ПОСЧИТАТЬ')

    return start, house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area, \
           ground_floor_height, num_of_rooms, double_bar_per, windows_area, slab_foundation, first_floor_area, floor_ceiling



#main script

#paths to folders with working data of models
working_path = os.getcwd()

#path to working models
models_path = working_path



#application header display
st.markdown('# CЕЙЧАС ВСЁ ПОСЧИТАЕМ!')

st.markdown('## Расчёт стоимости базового домокомплекта')

st.markdown('## Предваритеельный расчёт стоимости базового домокомплекта 2.0')


st.markdown('### Введите следующие данные')


#user input
start, house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area, ground_floor_height, \
num_of_rooms, double_bar_per, windows_area, slab_foundation, first_floor_area, floor_ceiling = input_transform_data()



#formation of input vector to be fed
#into the prediction CatBoost model
data = make_data_for_CB(house_type, attic_type, roof_type, roof_slope_angle, length, width, floor_area, veranda_area,
                        ground_floor_height, num_of_rooms, double_bar_per, windows_area)



#by pressing the сalculate button
if start:

    #flag for house or not house (bath, alcove)
    house_mode = 0
    if house_type == 'Дом':
        house_mode = 1

    #displaying a descriptive block based on user-entered data
    information_block_output (house_type, length, width, double_bar_per, attic_type, floor_area, veranda_area,
                              num_of_rooms, ground_floor_height, roof_type, roof_slope_angle, windows_area, floor_ceiling
                              )

    # prediction of the cost of a basic house kit
    # as the average prediction of the two best neural network models
    # and CatBoost models
    result(data, models_path, slab_foundation, first_floor_area, house_mode, floor_seiling, floor_area,
           roof_type, roof_slope_angle, attic_type)
