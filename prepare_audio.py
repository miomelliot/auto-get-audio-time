from pydub import AudioSegment
import os

def change_sample_rate(input_folder, output_folder, target_sample_rate):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получить список всех файлов WAV во входной папке
    wav_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.wav')]

    for filename in wav_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Загрузить аудиофайл
        sound = AudioSegment.from_file(input_path, format="wav")

        # Изменить частоту дискретизации
        sound = sound.set_frame_rate(target_sample_rate)

        # Сохранить файл с новой частотой дискретизации
        sound.export(output_path, format="wav")


input_folder = "аудио"
output_folder = "аудио для апи"
target_sample_rate = 8000

change_sample_rate(input_folder, output_folder, target_sample_rate)
