import subprocess, json, os, sys

BASE = os.path.expanduser("~/workspace/douyin/piying")
SCENES = [
    "media-generation-scene1-old-man-0-47e1a99f-3019-4c21-a9e4-c07d355333c1.webp",
    "media-generation-scene2-fox-alive-0-91a6422a-bd0d-4fc4-82df-5b5782c77a62.webp",
    "media-generation-scene3-fox-village-0-e57cd2b2-c648-43a8-9a16-0ae4843ae659.webp",
    "media-generation-scene4-dawn-0-f8bd49cf-49fc-4688-8119-b33001526f42.webp",
]
SUBS = [
    "从前，山脚下有个皮影村。\n村里老艺人最宝贝的，是一只红狐狸。",
    "这天夜里，灯影一晃，\n红狐狸从幕布上跳了下来，活了。",
    "小狐狸跑遍了整个村子，\n谁家孩子哭了，它就隔着窗纸跳一支舞。",
    "天亮前，小狐狸回到幕布上。\n从此，老艺人的戏，总比别人多一分灵气。",
]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
GAP = 0.7
FPS = 30

def dur(path):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",path])
    return float(json.loads(out)["format"]["duration"])

clips = []
for i in range(4):
    img = os.path.join(BASE,"scenes",SCENES[i])
    aud = os.path.join(BASE,"audio",f"narr{i+1}.mp3")
    d = dur(aud) + GAP
    frames = int(d*FPS)
    subfile = os.path.join(BASE,f"sub{i+1}.txt")
    with open(subfile,"w") as f: f.write(SUBS[i])
    clip = os.path.join(BASE,f"clip{i+1}.mp4")
    vf = (
        f"scale=1350:2400,"
        f"zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},"
        f"fade=t=in:st=0:d=0.5,fade=t=out:st={d-0.5:.2f}:d=0.5,"
        f"drawtext=fontfile={FONT}:textfile={subfile}:fontsize=46:fontcolor=white:borderw=3:bordercolor=black:"
        f"x=(w-text_w)/2:y=h-260:line_spacing=14,"
        f"format=yuv420p"
    )
    cmd = ["ffmpeg","-y","-loop","1","-i",img,"-i",aud,
           "-filter_complex",f"[0:v]{vf}[v];[1:a]apad=whole_dur={d:.2f},atrim=0:{d:.2f}[a]",
           "-map","[v]","-map","[a]","-t",f"{d:.2f}",
           "-c:v","libx264","-preset","medium","-crf","19","-c:a","aac","-b:a","160k","-ar","44100",
           clip]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"clip{i+1} FAILED"); print(r.stderr[-2000:]); sys.exit(1)
    clips.append(clip)
    print(f"clip{i+1} ok dur={d:.2f}s")

listfile = os.path.join(BASE,"clips.txt")
with open(listfile,"w") as f:
    for c in clips: f.write(f"file '{c}'\n")
final = os.path.join(BASE,"piying_fox_sample.mp4")
r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",listfile,"-c","copy",final],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-2000:]); sys.exit(1)
print("FINAL", final, "duration", dur(final))
