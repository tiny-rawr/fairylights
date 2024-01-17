import requests
import time
import whisper

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken by '{func.__name__}': {elapsed_time:.2f} seconds")
        return result

    return wrapper

@measure_time
def get_transcript(video_url="video.mp4"):
    model = whisper.load_model("base")
    result = model.transcribe(video_url)

    return result['text'] if result and 'text' in result else None

@measure_time
def save_transcript_to_file(transcript, filename="transcript.txt"):
    if transcript:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcript)
        print(f"Transcript saved as '{filename}'")
    else:
        print("No transcript available to save.")

if __name__ == "__main__":
    #video_url = "https://storage.googleapis.com/lablab-video-submissions/clqgrilce0007357efdiaaraq/raw/submission-video-x-clqgrilce0007357efdiaaraq-clraujx2a002d356r48muo5ms_0e3ztm00dp.mp4"
    video_url = "https://storage.googleapis.com/lablab-video-submissions/clexa6z2p0000356jf6xoq273%2Fraw%2Fsubmission-video-x-clexa6z2p0000356jf6xoq273-clfo80ucq00hu356hvyya36k4.mp4"

    print("Getting transcript")
    transcript_text = get_transcript(video_url)
    print("Save transcript to file")
    save_transcript_to_file(transcript_text)
