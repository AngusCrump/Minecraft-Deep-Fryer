import os, glob, ffmpy, shutil, threading, deep_fried_meme

fry_amount = 5
threads = 10

filepool = list()

for i in range(threads):
    filepool.append(list())

print(filepool)

out = "Deep Fried Minecraft"

def increase_audio(input_audio, amt, filename):
    output_args = ['-y', '-af', 'volume=3, bass=g=5, treble=g=-10']
    audio_file = None
    for idx in range(amt):
        input_file = audio_file or input_audio
        os.makedirs(f"tmp/tmp{idx}/{os.path.dirname(filename)}", exist_ok=True)
        output = f"tmp/tmp{idx}/{filename}"
        ff = ffmpy.FFmpeg(inputs={input_file: None}, outputs={output: output_args})
        ff.run()
        audio_file = output

    return audio_file



def fry_and_save(files):
    for filename in files:
        if filename.endswith(".ogg"):
            fried = increase_audio(filename, fry_amount, filename)
            os.makedirs(os.path.dirname(os.path.join(out, filename)), exist_ok=True)
            shutil.copy(fried, os.path.join(out, filename))
        
        if filename.endswith(".png"):
            os.makedirs(os.path.dirname(os.path.join(out, filename)), exist_ok=True)
            deep_fried_meme.deep_frier(filename, putout_scheme=['file', os.path.join(out, filename)[:-4], 'png'])


all_files = list(glob.iglob("minecraft/**", recursive=True))


while len(all_files) > 0:
    for b in range(threads):
        try:
            filepool[b].append(all_files[0])
        except:
            break
        del all_files[0]

threadlist = list()
for t in range(threads):
    threadlist.append(threading.Thread(target=fry_and_save, args=[filepool[t]]))

for t in threadlist:
    t.start()

for t in threadlist:
    t.join()
