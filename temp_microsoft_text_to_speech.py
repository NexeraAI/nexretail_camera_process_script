import os
import azure.cognitiveservices.speech as speechsdk

SPEECH_KEY = "b0a3dcdadcca4a13bf98c8aa09e52fc8"
SPEECH_REGION = "southeastasia"

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

text = "Hello！我是 T 醬，您的專屬TOYOTA虛擬銷售顧問！ 我專門負責COROLLA CROSS，無論是功能、配備都可以為您解答！您有什麼想了解的呢？都可以問我噢～"

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")