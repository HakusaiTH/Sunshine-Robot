import iapp_ai

# kaitom tts 
'''
def generate_and_play_audio(text):
    apikey = 'YWa92l0PnnG3ViGTtiZfdtJTiaro6iCG' #YWa92l0PnnG3ViGTtiZfdtJTiaro6iCG

    api = iapp_ai.api(apikey)

    output_file = "output.mp3"
    response = api.thai_thaitts_kaitom(text)

    with open(output_file, "wb") as f:
        f.write(response.content)

    return True
'''

from gtts import gTTS
import os

# google tts 
def generate_and_play_audio(text, lang='th'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    # os.system("start output.mp3")  # This command is for Windows. For other OS, you may need to use different commands.

# Example usage:
# generate_and_play_audio("phoovadet")

# generate_and_play_audio("สภาพอากาศ")