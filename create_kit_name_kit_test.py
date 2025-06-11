# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request

# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data

# Функция, которая меняет содержимое тела запроса
def get_kit_body(name):

    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.kit_body.copy()

    # изменение значения в поле name
    current_body["name"] = name

    # возвращается новый словарь с нужным значением name
    return current_body 

# Функция для получения токена
def get_new_user_token():
    # Создать нового клиента 
    user_body = data.user_body
    resp_user = sender_stand_request.post_new_user(user_body)

    # Запомнить токен авторизации 
    return resp_user.json()["authToken"]

# Функция для позитивной проверки
def positive_assert(kit_body):
    # Результат запроса на создание набора
    kit_response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert kit_response.status_code == 201
    
    # Проверяется, что в ответе поле name совпадает с name из запроса
    assert kit_response.json()["name"] == kit_body["name"]

# Функция для негативной проверки
def negative_assert_code_400(kit_body):

    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert response.status_code == 400
    

# Функция для негативной проверки 
def negative_assert_no_name(kit_body):
    # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert response.status_code == 400

    # Проверка текста в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1. Успешное создание набора
# Параметр name состоит из 1 символа
def test_create_kit_1_letter_in_name_get_success_response():
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body("a")
    positive_assert(kit_body)
    

# Тест 2. Успешное создание набора
# Параметр name состоит из 511 символов
def test_create_kit_511_letter_in_name_get_success_response():
    kit_body = get_kit_body("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")
    positive_assert(kit_body)

# Тест 3. Ошибка 
# Параметр name состоит из 0 символов
def test_create_kit_0_letter_in_name_get_error_response():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

# Тест 4. Ошибка 
# Параметр name состоит из 512 символов
def test_create_kit_512_letter_in_name_get_error_response():
    kit_body = get_kit_body("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert_code_400(kit_body)

# Тест 5. Успешное создание набора 
# Параметр name состоит из английских букв
def test_create_kit_english_letter_in_name_get_success_response():
    kit_body = get_kit_body("QWErty")
    positive_assert(kit_body)

# Тест 6. Успешное создание набора 
# Параметр name состоит из русских букв
def test_create_kit_russian__letter_in_name_get_success_response():
    kit_body = get_kit_body("Мария")
    positive_assert(kit_body)

# Тест 7. Успешное создание набора 
# Параметр name состоит из строки спецсимволов
def test_create_kit_has_special_symbol_in_name_get_success_response():
    kit_body = get_kit_body("\"№%@\",")
    positive_assert(kit_body)

# Тест 8. Успешное создание набора 
# Параметр name состоит из слов с пробелами
def test_create_kit_has_space_in_name_get_success_response():
    kit_body = get_kit_body("Человек и КО")
    positive_assert(kit_body)

# Тест 9. Успешное создание набора 
# Параметр name состоит из цифр
def test_create_kit_has_number_in_name_get_success_response():
    kit_body = get_kit_body("123")
    positive_assert(kit_body)

# Тест 10. Ошибка: в запросе нет параметра name
def test_create_kit_no_name_get_error_response():

    kit_body = data.kit_body.copy()
    # Удаление параметра name из запроса
    kit_body.pop("name")
    # Проверка полученного ответа
    negative_assert_no_name(kit_body)

# Тест 11. Ошибка: числовой тип параметра name
def test_create_kit_number_type_name_get_error_response():
    kit_body = get_kit_body(12)
    negative_assert_code_400(kit_body)