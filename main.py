import os
import yt_dlp
import whisper
from gtts import gTTS

BASE_PATH = r"C:\Users\Kleszczu\Desktop\Gedia mp3"
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)


def download_audio(youtube_url, output_path=BASE_PATH):
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"
        return mp3_file


def transcribe_audio(mp3_file, language=None, output_txt=None):

    if output_txt is None:
        output_txt = os.path.splitext(mp3_file)[0] + ".txt"

    model = whisper.load_model("base")

    if language:
        result = model.transcribe(mp3_file, language=language)
    else:
        result = model.transcribe(mp3_file)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print("Tłumaczenie ukończone!")
    return output_txt


def text_to_speech(txt_file, lang="pl", output_mp3=None):
    if output_mp3 is None:
        output_mp3 = os.path.splitext(txt_file)[0] + "_tts.mp3"

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    tts = gTTS(text=text, lang=lang)
    tts.save(output_mp3)
    print("Wygenerowano plik .mp3")
    return output_mp3


if __name__ == "__main__":
    link = input("Podaj link: ")
    mp3_path = download_audio(link)
    print("Plik pobrany")

    lang_choice = input("Podaj języka do tłumaczenia nagrania('pl' polski, 'en' angielski, 'de' niemiecki): ").strip()
    lang_choice = lang_choice if lang_choice else None

    txt_path = transcribe_audio(mp3_path, language=lang_choice)

    tts_lang = input("Podaj język dla syntezatora ('pl' polski, 'en' angielski, 'de' niemiecki): ").strip()
    tts_lang = tts_lang if tts_lang else "pl"

    text_to_speech(txt_path, lang=tts_lang)