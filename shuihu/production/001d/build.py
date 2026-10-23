import subprocess, json, os, sys
NEW = os.path.expanduser("~/workspace/douyin/shuihu/production/001d")
OLD = os.path.expanduser("~/workspace/douyin/shuihu/production/001/clips")
def nclip(name): return os.path.join(NEW,"clips",name)
def oclip(name): return os.path.join(OLD,name)
SHOTS = [
 nclip("media-generation-d1-shot01-court-0-2b2bf5c3-5a39-4c01-ad30-5d2636f63e87.mp4"),
 oclip("media-generation-r1-shot1-0-5ffc13a6-66e5-4b8a-969e-d867e8cc45ca.mp4"),
 nclip("media-generation-d1-shot03-memorial-0-8aed6c3e-80d1-4158-a649-c2c2cc34847a.mp4"),
 nclip("media-generation-d1-shot04-edict-0-a2c29e26-3812-430d-8393-177fb02df3d0.mp4"),
 oclip("media-generation-r1-shot2-0-fe0838a0-e13f-428b-a754-0f933c0d9f64.mp4"),
 nclip("media-generation-d1-shot06-welcome-0-059e3796-17c3-4fea-b4d5-1e21488a5d7f.mp4"),
 oclip("media-generation-r1-shot3-0-236ebe70-9a74-42a9-bfc5-f1662d881c3b.mp4"),
 nclip("media-generation-d1-shot08-abbot-0-b98fa16e-4ada-4f27-a502-9aa740d5b4b5.mp4"),
 oclip("media-generation-r1-shot4-0-9f856242-3d73-4e8d-8400-a5c6e26b8964.mp4"),
 oclip("media-generation-r1-shot5-0-e85c7fe3-9a2c-4586-8076-140d650d8d87.mp4"),
 nclip("media-generation-d1-shot11-smoke-0-4f4b1d95-dd08-4087-9aeb-3910d581f2ac.mp4"),
 oclip("media-generation-r1-shot6-0-67632e41-e64f-4038-9d9b-e8fd51da8027.mp4"),
]
SUBS = [
 "话说大宋仁宗嘉祐三年三月，\n皇帝驾坐紫宸殿，百官朝贺，好一派太平气象。",
 "可这太平底下藏着祸事：京师瘟疫盛行，\n伤损军民无数，家家闭户，人人掩口。",
 "宰相参政连番上奏，范仲淹越班启奏：\n要禳此灾，须宣嗣汉天师张真人\n星夜来朝，设罗天大醮。",
 "仁宗准奏，御笔亲书丹诏，\n钦差殿前太尉洪信，捧诏赍香，\n前往江西龙虎山。",
 "洪太尉领了圣敕，带了数十随从，\n上了铺马，离了东京，一路逶迤投信州而来。",
 "到了龙虎山下，上清宫道众鸣钟击鼓，\n香花灯烛，幢幡宝盖，\n一派仙乐下山迎接丹诏。",
 "次日太尉上山寻访天师，\n却在山道遇一牧童，倒骑黄牛，吹笛而来——\n那牧童正是张天师！",
 "住持告诉太尉：天师早知来意，\n已设醮祈禳完毕，驾鹤回天。\n说着领太尉来到伏魔之殿前：\n此殿封着三十六天罡、七十二地煞，\n先师遗训——遇洪而开。",
 "太尉听了大笑：什么魔君！\n这遇洪，说的正是我洪信！\n任凭道众苦劝，他偏要开殿。",
 "众人拦不住，太尉亲手揭了封条，\n掘开石碑，双手抵住石碑，用力推去。",
 "只听轰隆一声巨响，石碑倒地，\n黑气冲天而起，殿前众人纷纷后退。",
 "黑气化作一百零八道金光，散向九州大地。\n三十六天罡、七十二地煞，自此降临人间——\n梁山好汉的故事，就从这里开始！",
]
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
def dur(p):
    out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",p])
    return float(json.loads(out)["format"]["duration"])
segs = []
for i in range(12):
    vid = SHOTS[i]; aud = os.path.join(NEW,"audio",f"n{i+1:02d}.mp3")
    cd, ad = dur(vid), dur(aud)
    d = ad + 0.8
    subf = os.path.join(NEW,f"s{i+1:02d}.txt"); open(subf,"w").write(SUBS[i])
    base = "scale=720:1280,fps=24"
    if d > cd + 0.05:
        vpre = f"[0:v]{base},split[a][b];[b]reverse[br];[a][br]concat=n=2:v=1:a=0,setpts=PTS-STARTPTS[vv];"
        vin = "[vv]"
    else:
        vpre = ""; vin = "[0:v]"
    nlines = SUBS[i].count("\n") + 1
    ypos = 1280 - 64 - nlines * 40
    vf = (f"{base}," if not vpre else "") + \
         f"drawtext=fontfile={FONT}:textfile={subf}:fontsize=30:fontcolor=white:borderw=3:bordercolor=black:" \
         f"x=(w-text_w)/2:y={ypos}:line_spacing=10,format=yuv420p"
    if i == 0:
        tf = os.path.join(NEW,"title.txt"); open(tf,"w").write("第一回 洪太尉误走妖魔")
        vf = (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=46:fontcolor=white:borderw=3:bordercolor=black:"
              "x=(w-text_w)/2:y=100:enable='lt(t,3.5)'," + vf)
    fc = f"{vpre}{vin}{vf}[v];[1:a]apad=whole_dur={d:.2f},atrim=0:{d:.2f}[a]"
    out = os.path.join(NEW,f"seg{i+1:02d}.mp4")
    r = subprocess.run(["ffmpeg","-y","-i",vid,"-i",aud,"-filter_complex",fc,
                        "-map","[v]","-map","[a]","-t",f"{d:.2f}",
                        "-c:v","libx264","-preset","medium","-crf","23","-c:a","aac","-b:a","160k","-ar","44100",out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"seg{i+1} FAILED"); print(r.stderr[-1200:]); sys.exit(1)
    segs.append(out); print(f"seg{i+1} ok {d:.2f}s (clip {cd:.1f}s)")
lf = os.path.join(NEW,"segs.txt"); open(lf,"w").write("".join(f"file '{s}'\n" for s in segs))
final = os.path.join(NEW,"final_detailed.mp4")
r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lf,"-c","copy",final], capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-1200:]); sys.exit(1)
print("FINAL", final, "dur", dur(final))
