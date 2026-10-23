import subprocess, json, os, sys
# 水浒传第2回（说书旁白版，14镜）合成脚本
# 用法：镜头 14/14 + 配音 n01–n14 齐全后运行：python3 build.py
BASE = os.path.expanduser("~/workspace/douyin/shuihu/production/002")
SHOTS = [os.path.join(BASE, "clips", f"shot{i}.mp4") for i in range(1, 15)]
SUBS = [
 "话说洪太尉放走了妖魔，冷汗淋漓，\n连夜回京。天师早已在京中做了七昼夜\n道场，瘟疫尽消。可那一百零八个魔君\n下山，这天下，从此就不太平了。",
 "仁宗在位四十二年，\n此后英宗、神宗相继而立。\n到了哲宗年间，天下太平，四方无事。\n东京城里，却出了一个日后的大祸害。",
 "这人姓高，排行第二，人称高毬。\n刺枪使棒样样来得，\n最绝的是一脚好气毬。\n可他仁义礼智信一概不会，\n就是个帮闲的破落户。",
 "他帮人使钱惹出官司，\n被开封府打了二十脊杖，赶出东京城。\n流落淮西三年，直到哲宗皇帝大赦\n天下，才又回到京师。",
 "回京后他投亲访友，家家都不敢留：\n董将士推给小苏学士，\n学士又推给小王都太尉。\n这太尉是皇帝的妹夫，\n偏偏就喜欢这样的人。",
 "一日，端王在府中踢球，气毬飞来，\n高俅露了一手绝活，\n颠得端王眉开眼笑，\n当场就把他留在了身边。\n这个端王，就是日后的宋徽宗。",
 "不出半年，端王登基做了皇帝。\n高俅这泼皮，竟然一夜之间\n当上了殿帅府太尉。\n真是：朝为市井无赖，暮登天子堂前。",
 "高俅新官上任，第一天就寻起旧仇：\n王进的父亲当年曾一棒打得他三月不起。\n这日点卯，他借故王进装病不到，\n咬牙要拿他出气。",
 "王进听得风声，知道这祸躲不过。\n当夜他装作看病，扶着老母，\n弃了官职，悄悄出了东京城，\n直投延安府老种经略相公处去。",
 "行到华阴县史家村，天降大雨，\n王进母子在庄前借宿。\n史太公是个好客的老人家，\n连忙迎进庄里，酒饭相待。",
 "次日，王进听见后院喝彩。\n只见一个少年赤着膊，\n身上刺着九条青龙，正使一条棒，\n满院生风。这便是史太公的儿子，\n江湖人称九纹龙史进。",
 "史进不服，要与王进比试。\n王进只一合就拨开了他的棒，\n随即一条枪舞得神出鬼没。\n史进看得呆了，推金山倒玉柱，\n纳头便拜。",
 "史进拜王进为师，\n冬练三九，夏练三伏，\n十八般武艺件件精通。\n半年之后，王进辞别太公，\n望延安府去了。",
 "不久史太公病逝，史进当了家。\n这日少华山好汉陈达来借粮，\n史进披挂出庄，只一合便把陈达\n活捉回来。九纹龙的名号，\n从此响遍江湖。",
]
TITLE = "第二回 九纹龙大闹史家村"
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
def dur(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                   "format=duration", "-of", "json", p])
    return float(json.loads(out)["format"]["duration"])
segs = []
for i in range(14):
    vid = SHOTS[i]; aud = os.path.join(BASE, "audio", f"n{i+1:02d}.mp3")
    if not os.path.exists(vid):
        print(f"缺少镜头 {vid}，停止"); sys.exit(2)
    if not os.path.exists(aud):
        print(f"缺少配音 {aud}，停止"); sys.exit(2)
    cd, ad = dur(vid), dur(aud)
    d = ad + 0.8
    subf = os.path.join(BASE, f"s{i+1:02d}.txt"); open(subf, "w").write(SUBS[i])
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
        tf = os.path.join(BASE, "title.txt"); open(tf, "w").write(TITLE)
        vf = (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=46:fontcolor=white:borderw=3:bordercolor=black:"
              "x=(w-text_w)/2:y=100:enable='lt(t,3.5)'," + vf)
    fc = f"{vpre}{vin}{vf}[v];[1:a]apad=whole_dur={d:.2f},atrim=0:{d:.2f}[a]"
    out = os.path.join(BASE, f"seg{i+1:02d}.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-i", vid, "-i", aud, "-filter_complex", fc,
                        "-map", "[v]", "-map", "[a]", "-t", f"{d:.2f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                        "-c:a", "aac", "-b:a", "160k", "-ar", "44100", out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"seg{i+1} FAILED"); print(r.stderr[-1200:]); sys.exit(1)
    segs.append(out); print(f"seg{i+1} ok {d:.2f}s (clip {cd:.1f}s)")
lf = os.path.join(BASE, "segs.txt"); open(lf, "w").write("".join(f"file '{s}'\n" for s in segs))
final = os.path.join(BASE, "final.mp4")
r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lf, "-c", "copy", final],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("concat FAILED"); print(r.stderr[-1200:]); sys.exit(1)
print("FINAL", final, "dur", dur(final))
