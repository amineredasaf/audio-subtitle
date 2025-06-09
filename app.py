from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import wave
import json
import os
import srt
from datetime import timedelta
from vosk import Model, KaldiRecognizer
import uuid
import shutil
import tempfile
import subprocess

app = FastAPI()

MODEL_PATH = "./vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

def convert_audio(input_path, output_path):
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", "-f", "wav", output_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")

def transcribe(audio_path):
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    segments = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if "result" in res:
                words = res["result"]
                if words:
                    start = words[0]["start"]
                    end = words[-1]["end"]
                    text = " ".join([w["word"] for w in words])
                    segments.append((start, end, text))
    final_res = json.loads(rec.FinalResult())
    if "result" in final_res:
        words = final_res["result"]
        if words:
            start = words[0]["start"]
            end = words[-1]["end"]
            text = " ".join([w["word"] for w in words])
            segments.append((start, end, text))
    return segments

def generate_srt(segments, max_words_per_segment=8):
    subtitles = []
    idx = 1
    for start, end, text in segments:
        words = text.split()
        total_words = len(words)
        duration = end - start

        num_segments = (total_words + max_words_per_segment - 1) // max_words_per_segment
        segment_duration = duration / num_segments if num_segments > 0 else 0

        for i in range(num_segments):
            segment_start = start + i * segment_duration
            segment_end = segment_start + segment_duration

            chunk_words = words[i * max_words_per_segment : (i + 1) * max_words_per_segment]
            chunk_text = " ".join(chunk_words)

            subtitles.append(srt.Subtitle(
                index=idx,
                start=timedelta(seconds=segment_start),
                end=timedelta(seconds=segment_end),
                content=chunk_text
            ))
            idx += 1

    return srt.compose(subtitles)

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, f"{uuid.uuid4()}_{file.filename}")
            wav_path = os.path.join(tmpdir, "converted.wav")

            with open(input_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            convert_audio(input_path, wav_path)
            segments = transcribe(wav_path)
            srt_text = generate_srt(segments)

            return srt_text

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
