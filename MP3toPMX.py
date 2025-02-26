import json
import base64
from pydub import AudioSegment
import tempfile

def mp3_to_pmx(mp3_file, pmx_file):
    # Конвертируем MP3 в сжатый формат OGG
    audio = AudioSegment.from_mp3(mp3_file)
    
    # Экспорт в OGG (сжатый формат)
    ogg_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg")
    audio.export(ogg_file.name, format="ogg")
    
    # Чтение OGG-файла и конвертация в base64
    with open(ogg_file.name, "rb") as ogg_f:
        audio_base64 = base64.b64encode(ogg_f.read()).decode('utf-8')
    
    # Удаляем временный файл
    ogg_file.close()
    
    # Создание PMX-файла с аудио в base64
    pmx_data = {
        "audio": audio_base64  # Аудиофайл в base64 (сжатый)
    }
    
    # Сохраняем PMX-файл
    with open(pmx_file, "w") as f:
        json.dump(pmx_data, f, indent=2)
    
    print(f"Файл {pmx_file} успешно создан!")

# Использование
mp3_to_pmx("input.mp3", "output.pmx")
