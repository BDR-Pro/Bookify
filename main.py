from gradio_client import Client
from pytube import YouTube
link="https://www.youtube.com/watch?v=nY1gLtj7Sso&ab_channel=%D8%AC%D9%88%D8%A7%D9%87%D8%B1%D8%B9%D8%AF%D9%86%D8%A7%D9%86%D8%A5%D8%A8%D8%B1%D8%A7%D9%87%D9%8A%D9%85"

def fix_arabic(text):
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    return get_display(reshape(text))

def download(link):
    yt = YouTube(link)
    print("Downloading...")
    print(fix_arabic(yt.title))
    yt.streams.filter(only_audio=True).first().download(output_path="audio/", filename=yt.title+".mp3") 
    print("Downloaded")
    return "audio/"+yt.title+".mp3"

def title(link):
    yt = YouTube(link)
    return (yt.title)

client = Client("https://openai-whisper.hf.space/")
result = client.predict(
				download(link),	# str (filepath or URL to file) in 'inputs' Audio component
				"transcribe",	# str in 'Task' Radio component
				api_name="/predict"
)


#If the video in arabic
printable_result=fix_arabic(result)

# Print or use the bidi_text
print(printable_result)


# Form the filename with path to the subfolder
filename = "text/" + title(link) + ".txt"

# Open the file in write mode and write the result to it
with open(filename, "w", encoding='utf-8') as file:
    file.write(result)