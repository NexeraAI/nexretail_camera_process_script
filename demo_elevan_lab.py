from elevenlabs import ElevenLabs
import time

client = ElevenLabs(
    api_key="sk_8da5503b4b009e4fc4d7e07cd117175caa4471da9aa1a41e",
)
start_time = time.time()

response = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    model_id="eleven_multilingual_v2",
    text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
)

save_file_path = "output/output.mp3"

with open(save_file_path, "wb") as f:
    for chunk in response:
        if chunk:
            f.write(chunk)

print(f"{save_file_path}: A new audio file was saved successfully!")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.2f} seconds")