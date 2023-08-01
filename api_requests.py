import os
import requests
import json
import concurrent.futures

def process_request(url, params, input_file, output_folder):
    # Загрузить аудиофайл

    with open(input_file, "rb") as file:
        files = {"file": (os.path.basename(input_file), file, "audio/wav")}
   
        # Отправить POST-запрос с параметрами и аудиофайлом
        response = requests.post(url, data=params, files=files)

        if response.json()["ok"]==True:
            # Сохранить ответ в файл
            output_path = os.path.join(output_folder, os.path.basename(input_file))
            with open(output_path, "wb") as output_file:
                output_file.write(response.content)
            print("Ответ сохранен в:", output_path)
        else:
            print(f"Произошла ошибка при обработке файла {input_file}.")
            print(response.json())

def main():
    url = "https://paidmethods.mcn.ru/api/private/api/speech/brandVoice"  # Укажите URL для отправки POST-запроса

    with open("marks.json", "r", encoding='utf-8') as params_file:
        parameters = json.load(params_file)

    input_folder = "аудио для апи"
    output_folder = "ответы от апи 2"
    accountID=121079

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in parameters:
            filename=i.replace(':','_')+" 2.wav"
            param=parameters[i]
            param["accountID"]=accountID
            input_path = os.path.join(input_folder, filename)
            futures.append(executor.submit(process_request, url, param, input_path, output_folder))

        # Дождаться завершения всех запросов
        concurrent.futures.wait(futures)

main()
