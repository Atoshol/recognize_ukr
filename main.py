from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import os
import speech_recognition as sr
import types
from pydub import AudioSegment
from pydub.utils import make_chunks

def chose_file():
    files = os.listdir('chunks')
    if not files:
        files = sorted(os.listdir('chunks'), key=lambda fname: int(fname.split('.')[0]))
        for filename in files:
            os.remove(f'chunks/{filename}')
    else:
        pass

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    myaudio = AudioSegment.from_file(filename, "wav")
    chunk_length_ms = 60000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

    # Export all of the individual chunks as wav files

    for i, chunk in enumerate(chunks):
        chunk_name = "{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(f'chunks/{chunk_name}', format="wav")
    result.insert(1.0, 'FINISH CUT\n')


def create_text():
    files = os.listdir('chunks')
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    files = sorted(files, key=lambda fname: int(fname.split('.')[0]))

    with open('result_text.txt', 'w') as txt_file:
        r = sr.Recognizer()
        for filename in files:
            if filename != '.DS_Store':
                with sr.AudioFile(f'chunks/{filename}') as source:
                    audio_data = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
                    try:

                        # using google speech recognition
                        text = r.recognize_google(audio_data, language='uk-UA')
                        print(f'readed chunk: {filename}')
                        txt_file.writelines(text)
                        txt_file.write('\n')
                        txt_file.write('\n')
                        txt_file.flush()

                    except:
                        print('Sorry.. run again...')
                os.remove(f'chunks/{filename}')
            else:
                continue
    result.insert(1.0, 'FINISH RECOGNIZE')


root = Tk()
root.title("recognize_ukr")
l1 = Label(root, text='Step 1: ', bg='#D3D3D3')
l1.grid(row=1, column=0)
button = Button(text='Choose file', command=chose_file, width=10, height=3, bg='#D3D3D3')
button.grid(row=1, column=1)
l1 = Label(root, text='Step 2: ', bg='#D3D3D3')
l1.grid(row=2, column=0)
button = Button(text='Start recognize', command=create_text, width=10, height=3, bg='#D3D3D3')
button.grid(row=2, column=1)
result = Text(root, width=37, height=5)
result.grid(row=4, column=0, rowspan=2)


root.geometry("400x300")
root.mainloop()
