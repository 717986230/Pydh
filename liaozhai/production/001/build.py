import subprocess, json, os, sys
BASE = os.path.expanduser("~/workspace/douyin/liaozhai/production/001")
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
GAP = 0.35

# shot -> [(linefile, speaker, text)]
LINES = {
 1: [("line01","王生","听说崂山多仙人！我王七今日上山，定要学成仙法！")],
 2: [("line02","道士","学道先要吃苦。你这富家子弟，受得了吗？"),("line03","王生","能！弟子能吃苦！")],
 3: [("line04","同门","师弟，手脚麻利些，跟上！"),("line05","王生","来了来了……")],
 4: [("line06","王生","一个月了……这哪是学仙，分明是当樵夫。")],
 5: [("line07","王生","一张纸……变成月亮了？！")],
 6: [("line08","客甲","今夜良宵，诸位尽管喝，这酒——喝不尽！")],
 7: [("line09","嫦娥","仙仙乎，而还乎，而幽我于广寒乎……")],
 8: [("line10","王生","他们……进月亮里喝酒去了！这才是真仙法！")],
 9: [("line11","王生","师父，弟子学了两个月，只学会砍柴……"),("line12","道士","我早说过，你吃不了苦。明早下山去吧。")],
 10: [("line13","王生","求师父教我一个小法术，就一个，不枉我来这一趟！"),("line14","道士","你想学哪样？"),("line15","王生","穿墙！就学穿墙！")],
 11: [("line16","王生","过去了！我过去了！"),("line17","道士","回去须洁身自持，否则——不灵。")],
 12: [("line18","王生","看好了，仙法——穿墙！"),("line19","妻","你的仙法，就这？哈哈哈！"),("line20","王生","老道士……他骗我！")],
}

def dur(p):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",p])
    return float(json.loads(out)["format"]["duration"])

def wrap(text, n=16):
    out=[]
    while len(text)>n:
        cut=n
        for p in "，。！？；、——……":
            i=text.rfind(p,0,n+1)
            if i>=6: cut=i+1; break
        out.append(text[:cut]); text=text[cut:]
    out.append(text)
    return "\n".join(out)

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0:
        print("FAILED:", " ".join(cmd)[:200]); print(r.stderr[-1500:]); sys.exit(1)
    return r

# silence file
sil=os.path.join(BASE,"sil.mp3")
if not os.path.exists(sil):
    run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-t",str(GAP),"-c:a","libmp3lame",sil])

segs=[]
for shot in range(1,13):
    clip=os.path.join(BASE,"clips",f"shot{shot}.mp4")
    items=LINES[shot]
    # build shot audio: concat lines with gaps
    lst=os.path.join(BASE,f"al{shot:02d}.txt")
    parts=[]
    with open(lst,"w") as f:
        for j,(lf,sp,tx) in enumerate(items):
            f.write(f"file '{os.path.join(BASE,'audio',lf+'.mp3')}'\n")
            if j<len(items)-1: f.write(f"file '{sil}'\n")
    shot_aud=os.path.join(BASE,f"shot{shot:02d}_audio.mp3")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c:a","libmp3lame","-ar","44100",shot_aud])
    # timings
    offs=[]; t=0.15
    for (lf,sp,tx) in items:
        d=dur(os.path.join(BASE,"audio",lf+".mp3")); offs.append((t,t+d,sp,tx)); t+=d+GAP
    ad=dur(shot_aud); cd=dur(clip)
    D=max(cd, ad+0.7)
    # video source: ping-pong extend if needed
    vsrc=clip
    if D>cd+0.05:
        pp=os.path.join(BASE,f"pp{shot:02d}.mp4")
        run(["ffmpeg","-y","-stream_loop","-1","-i",clip,"-filter_complex",
             "[0:v]split[a][b];[b]reverse[br];[a][br]concat=n=2:v=1:a=0,setpts=PTS-STARTPTS,trim=duration="+f"{D:.2f}"+"[v]",
             "-map","[v]","-c:v","libx264","-preset","medium","-crf","23","-an",pp])
        vsrc=pp
    # drawtext chain
    filters=["scale=720:1280","fps=24"]
    for (s0,s1,sp,tx) in offs:
        disp=f"{sp}：{tx}"
        w=wrap(disp)
        tf=os.path.join(BASE,f"st{shot:02d}_{int(s0*10)}.txt"); open(tf,"w").write(w)
        nl=w.count("\n")+1; y=1280-64-nl*40
        filters.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=30:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y={y}:line_spacing=10:enable='between(t,{s0:.2f},{s1+0.25:.2f})'")
    if shot==1:
        tf=os.path.join(BASE,"title.txt"); open(tf,"w").write("聊斋志异 · 崂山道士")
        filters.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=46:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=100:enable='lt(t,3.5)'")
    filters.append("format=yuv420p")
    out=os.path.join(BASE,f"seg{shot:02d}.mp4")
    run(["ffmpeg","-y","-i",vsrc,"-i",shot_aud,"-filter_complex",
         "[0:v]"+",".join(filters)+f"[v];[1:a]apad=whole_dur={D:.2f},atrim=0:{D:.2f}[a]",
         "-map","[v]","-map","[a]","-t",f"{D:.2f}",
         "-c:v","libx264","-preset","medium","-crf","23","-c:a","aac","-b:a","160k","-ar","44100",out])
    segs.append(out); print(f"seg{shot} ok {D:.2f}s (clip {cd:.1f}s, audio {ad:.1f}s)")

# end card
card=os.path.join(BASE,"seg13.mp4")
ct=os.path.join(BASE,"card.txt"); open(ct,"w").write("异史氏曰\n世之为王生者，正复不少。")
run(["ffmpeg","-y","-f","lavfi","-i","color=c=0xf3e9d2:s=720x1280:r=24:d=3","-f","lavfi","-i","anullsrc=r=44100:cl=stereo",
     "-filter_complex",f"[0:v]drawtext=fontfile={FONT}:textfile={ct}:fontsize=40:fontcolor=0x3a2a18:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=16,format=yuv420p[v]",
     "-map","[v]","-map","1:a","-t","3","-c:v","libx264","-preset","medium","-crf","23","-c:a","aac","-b:a","160k","-ar","44100",card])
segs.append(card); print("end card ok")

lf=os.path.join(BASE,"segs.txt"); open(lf,"w").write("".join(f"file '{s}'\n" for s in segs))
final=os.path.join(BASE,"final.mp4")
run(["ffmpeg","-y","-f","concat","-safe","0","-i",lf,"-c","copy",final])
print("FINAL", final, "dur", dur(final))
