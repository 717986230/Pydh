import subprocess, os, sys
BASE = os.path.expanduser("~/workspace/douyin/shuihu/ch01")
CLIPS = [
 ("media-generation-ch01-shot1-plague-city-0-582d1640-1858-4c1c-aa19-aed5c004290d.mp4","京城瘟疫，仁宗忧心"),
 ("media-generation-ch01-shot2-journey-0-ebc3520d-178f-4871-8b2f-d3969b013f72.mp4","洪太尉奉旨，上龙虎山"),
 ("media-generation-ch01-shot3-boy-tianshi-0-a1a62f8f-0d14-47c4-8c2d-8dde27635b52.mp4","牧童骑牛，原是张天师"),
 ("media-generation-ch01-shot4-stele-hall-0-4093611a-8a89-4eec-9b6c-bd1b2aedab4c.mp4","祈禳已毕，太尉闯伏魔殿"),
]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
outs = []
for i,(fn,cap) in enumerate(CLIPS,1):
    src = os.path.join(BASE,"clips",fn)
    capf = os.path.join(BASE,f"cap{i}.txt")
    open(capf,"w").write(cap)
    vf = (f"drawtext=fontfile={FONT}:textfile={capf}:fontsize=40:fontcolor=white:borderw=3:bordercolor=black:"
          f"x=(w-text_w)/2:y=h-110")
    if i == 1:
        tf = os.path.join(BASE,"title.txt"); open(tf,"w").write("第一回 洪太尉误走妖魔")
        vf += (f",drawtext=fontfile={FONT}:textfile={tf}:fontsize=54:fontcolor=white:borderw=3:bordercolor=black:"
               f"x=(w-text_w)/2:y=120:enable='lt(t,3.5)'")
    out = os.path.join(BASE,f"seg{i}.mp4")
    r = subprocess.run(["ffmpeg","-y","-i",src,"-vf",vf,"-an","-c:v","libx264","-preset","medium","-crf","20",
                        "-r","24","-pix_fmt","yuv420p",out], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"seg{i} FAILED"); print(r.stderr[-1500:]); sys.exit(1)
    outs.append(out); print(f"seg{i} ok")
lf = os.path.join(BASE,"segs.txt")
open(lf,"w").write("".join(f"file '{o}'\n" for o in outs))
final = os.path.join(BASE,"shuihu_ch01.mp4")
r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lf,"-c","copy",final], capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-1500:]); sys.exit(1)
d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",final]).decode().strip()
print("FINAL", final, "dur", d)
