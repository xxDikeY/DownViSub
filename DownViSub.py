# pip install pytube
from pytube import Playlist

# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter


# Список для проверки запрещённых символов в названии файлов
char_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

while True:
    try:
        # Ссылка на плейлист
        #playlist = Playlist(input("Введите ссылку на плейлист: "))
        playlist = Playlist("https://www.youtube.com/playlist?list=PL3v6p1kJaY-jLLgxL-IZGQT1ZAjrmtS1f")

        all_count = len(playlist.videos)
        count = 1

    except:
        print("Неправильно введена ссылка")
        continue

    break




for video in playlist.videos:

    print("_________________________________________")

    # Название видео
    video_name = video.title

    # Проверка на имя видео
    for char in char_list:
        if video_name.find(char) != -1:
            video_name = video_name.replace(char, " ")

    print(f"Скачивание видео: {count}/{all_count}\n{video_name}")

    # Скачивание видео в 360p
    video.streams.get_by_itag(18).download(f"{video_name}/")

    # Список со всеми субтитрами
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video.video_id)
        # Подготовка для формата файла srt
        formatter = SRTFormatter()


        for transcript in transcript_list:

            print(f"Скачивание субтитров: {transcript.language}")

            # Найти языковой код в списке
            try:
                tr = transcript_list.find_manually_created_transcript([transcript.language_code])
                lang_code = transcript.language_code

            # Если только автоматически сгенерированные субтитры
            except:
                tr = transcript_list.find_generated_transcript([transcript.language_code])
                lang_code = transcript.language_code + "-a"

            # Генирация текста в формате srt
            srt_formatted = formatter.format_transcript(tr.fetch())

            # Запись субтитров в файл с именем: "[код языка] [название видео].srt"
            with open(f'{video_name}/[{lang_code}] {video_name}.srt', 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt_formatted)
    
    # Если субтитров нет
    except:
        print("Субтитров нет")
    

    count += 1

input("Завершено")