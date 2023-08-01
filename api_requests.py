import os
import requests
import json
import concurrent.futures

def process_request(url, params, input_file, output_folder):
    # Загрузить аудиофайл
    with open(input_file, "rb") as file:
        files = {"audio": (os.path.basename(input_file), file, "audio/wav")}

        # Отправить POST-запрос с параметрами и аудиофайлом
        response = requests.post(url, data=params, files=files)

        if response.status_code == 200:
            # Сохранить ответ в файл
            output_path = os.path.join(output_folder, os.path.basename(input_file))
            with open(output_path, "wb") as output_file:
                output_file.write(response.content)
            print("Ответ сохранен в:", output_path)
        else:
            print(f"Произошла ошибка при обработке файла {input_file}.")
            print("Код ошибки:", response.status_code)
            print("Текст ошибки:", response.text)

def main():
    url = "https://paidmethods.mcn.ru/api/private/api/speech/brandVoice"  # Укажите URL для отправки POST-запроса

    with open("marks.json", "r") as params_file:
        parameters = json.load(params_file)

    input_folder = "аудио для апи"
    output_folder = "ответы от апи"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получить список всех файлов WAV в папке
    wav_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.wav')]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in wav_files:
            input_path = os.path.join(input_folder, filename)
            futures.append(executor.submit(process_request, url, parameters, input_path, output_folder))

        # Дождаться завершения всех запросов
        concurrent.futures.wait(futures)

main()