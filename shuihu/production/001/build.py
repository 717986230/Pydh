import subprocess, json, os, sys, glob
BASE = os.path.expanduser("~/workspace/douyin/shuihu/production/001")
CLIPS = sorted(glob.glob(os.path.join(BASE,"clips","*.mp4")))
assert len(CLIPS) == 6, CLIPS
SUBS = [
 "话说大宋仁宗嘉祐三年，天下瘟疫横行，\n京城百姓十病九家，仁宗皇帝夜不能寐。",
 "仁宗传旨，命洪太尉赶往龙虎山，\n宣请张天师祈禳瘟疫。太尉星夜启程。",
 "山道之上，太尉遇一牧童：\n倒骑黄牛，吹笛而来。这牧童正是张天师！",
 "天师早已设醮祈禳完毕，飘然而去。\n太尉游山，偏偏闯进了伏魔之殿。",
 "道众苦劝不住，太尉揭去封条，推倒石碑——\n只听轰隆一声，黑气冲天而起！",
 "黑气化作一百零八道金光，散向九州大地。\n三十六天罡、七十二地煞降临人间，\n梁山好汉的故事，就从这里开始。",
]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
def dur(p):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",p])
    return float(json.loads(out)["format"]["duration"])
segs = []
for i in range(6):
    vid, aud = CLIPS[i], os.path.join(BASE,"audio",f"n{i+1}.mp3")
    d = min(dur(aud) + 0.8, dur(vid))
    subf = os.path.join(BASE,f"s{i+1}.txt"); open(subf,"w").write(SUBS[i])
    vf = (f"scale=720:1280,"
          f"drawtext=fontfile={FONT}:textfile={subf}:fontsize=34:fontcolor=white:borderw=3:bordercolor=black:"
          "x=(w-text_w)/2:y=h-190:line_spacing=10,format=yuv420p")
    if i == 0:
        tf = os.path.join(BASE,"title.txt"); open(tf,"w").write("第一回 洪太尉误走妖魔")
        vf = (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=46:fontcolor=white:borderw=3:bordercolor=black:"
              "x=(w-text_w)/2:y=100:enable='lt(t,3.5)'," + vf)
    out = os.path.join(BASE,f"seg{i+1}.mp4")
    fc = f"[0:v]{vf}[v];[1:a]apad=whole_dur={d:.2f},atrim=0:{d:.2f}[a]"
    r = subprocess.run(["ffmpeg","-y","-i",vid,"-i",aud,"-filter_complex",fc,
                        "-map","[v]","-map","[a]","-t",f"{d:.2f}",
                        "-c:v","libx264","-preset","medium","-crf","23","-c:a","aac","-b:a","160k","-ar","44100",out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"seg{i+1} FAILED"); print(r.stderr[-1200:]); sys.exit(1)
    segs.append(out); print(f"seg{i+1} ok {d:.2f}s")
lf = os.path.join(BASE,"segs.txt"); open(lf,"w").write("".join(f"file '{s}'\n" for s in segs))
final = os.path.join(BASE,"final.mp4")
r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lf,"-c","copy",final], capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-1200:]); sys.exit(1)
print("FINAL", final, "dur", dur(final))
