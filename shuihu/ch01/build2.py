import subprocess, json, os, sys
BASE = os.path.expanduser("~/workspace/douyin/shuihu/ch01")
CLIPS = [
 "media-generation-ch01-shot1-plague-city-0-582d1640-1858-4c1c-aa19-aed5c004290d.mp4",
 "media-generation-ch01-shot2-journey-0-ebc3520d-178f-4871-8b2f-d3969b013f72.mp4",
 "media-generation-ch01-shot3-boy-tianshi-0-a1a62f8f-0d14-47c4-8c2d-8dde27635b52.mp4",
 "media-generation-ch01-shot4-stele-hall-0-4093611a-8a89-4eec-9b6c-bd1b2aedab4c.mp4",
]
SUBS = [
 "话说宋仁宗嘉祐年间，天下瘟疫横行，\n京城百姓十病九家，仁宗皇帝夜不能寐。",
 "仁宗传下圣旨，命洪太尉星夜赶往龙虎山，\n宣请张天师，祈禳瘟疫。",
 "太尉在山道上遇见一牧童，倒骑黄牛，吹笛而来。\n谁能想到，这牧童正是张天师！",
 "祈禳已毕，太尉偏要游那伏魔之殿。\n道众拦不住，他迈步就往石碑跟前闯。",
]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
def dur(p):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",p])
    return float(json.loads(out)["format"]["duration"])
segs = []
for i in range(4):
    vid = os.path.join(BASE,"clips",CLIPS[i])
    aud = os.path.join(BASE,"audio",f"n{i+1}.mp3")
    d = dur(aud) + 0.8
    subf = os.path.join(BASE,f"s{i+1}.txt"); open(subf,"w").write(SUBS[i])
    vf = ("eq=saturation=0.68:contrast=1.07:brightness=-0.02,noise=alls=16:allf=t,"
          f"drawtext=fontfile={FONT}:textfile={subf}:fontsize=38:fontcolor=white:borderw=3:bordercolor=black:"
          "x=(w-text_w)/2:y=h-170:line_spacing=12,format=yuv420p")
    if i == 0:
        tf = os.path.join(BASE,"title.txt"); open(tf,"w").write("第一回 洪太尉误走妖魔")
        vf = (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=52:fontcolor=white:borderw=3:bordercolor=black:"
              "x=(w-text_w)/2:y=110:enable='lt(t,3.5)'," + vf)
    out = os.path.join(BASE,f"vseg{i+1}.mp4")
    fc = f"[0:v]{vf}[v];[1:a]apad=whole_dur={d:.2f},atrim=0:{d:.2f}[a]"
    r = subprocess.run(["ffmpeg","-y","-i",vid,"-i",aud,"-filter_complex",fc,
                        "-map","[v]","-map","[a]","-t",f"{d:.2f}",
                        "-c:v","libx264","-preset","medium","-crf","20","-c:a","aac","-b:a","160k","-ar","44100",out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"vseg{i+1} FAILED"); print(r.stderr[-1500:]); sys.exit(1)
    segs.append(out); print(f"vseg{i+1} ok {d:.2f}s")
lf = os.path.join(BASE,"vsegs.txt"); open(lf,"w").write("".join(f"file '{s}'\n" for s in segs))
final = os.path.join(BASE,"shuihu_ch01_v2.mp4")
r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lf,"-c","copy",final], capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-1500:]); sys.exit(1)
print("FINAL", final, "dur", dur(final))
