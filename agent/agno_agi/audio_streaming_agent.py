import base64
import wave
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import Iterator
from agno.agent import RunResponse  # Import RunResponse
import wave
import pyaudio

# Audio Configuration
SAMPLE_RATE = 24000  # Hz (24kHz)
CHANNELS = 1  # Mono
SAMPLE_WIDTH = 2  # Bytes (16 bits)
#         stream.stop_stream()
#         stream.close()
#         p.terminate()


agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={
            "voice": "alloy",
            "format": "pcm16",  # Required for streaming
        },
    ),
    # debug_mode=True,
    add_history_to_messages=True,
)

# Question with streaming
output_stream: Iterator[RunResponse] = agent.run(
    "Kể một câu chuyện hài dưới 100 từ", 
    stream=True
)

with wave.open("tmp/answer_1.wav", "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(SAMPLE_WIDTH)
    wav_file.setframerate(SAMPLE_RATE)
    # Khởi tạo PyAudio để phát âm thanh
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True)
    #============================
    try:
        for response in output_stream:
            if response.response_audio:
                if response.response_audio.transcript:
                    print(response.response_audio.transcript, end="", flush=True)
                if response.response_audio.content:
                    try:
                        pcm_bytes = base64.b64decode(response.response_audio.content)
                        wav_file.writeframes(pcm_bytes)
                        stream.write(pcm_bytes)  # Phát âm thanh trực tiếp
                    except Exception as e:
                        print(f"Error decoding audio: {e}")
    finally:
        # Đóng stream âm thanh
        stream.stop_stream()
        stream.close()
        p.terminate()                    

# print()
# with wave.open("tmp/answer_1.wav", "rb") as wav_file:
#     # Đọc dữ liệu từ file và phát âm thanh
#     play_audio_stream(iter(lambda: wav_file.readframes(1024), b""))
        