import configuration
import requests
import data

# Функция post_new_user для создания пользователя
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

# Функция post_new_client_kit для создания набора
def post_new_client_kit(kit_body, auth_token): 
    headers_dict = data.headers.copy() 
    headers_dict["Authorization"] = "Bearer " + auth_token; 
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,
                         json=kit_body, 
                         headers=headers_dict) # не только токен, но и из data; формат для записи в headers — ключ-значение