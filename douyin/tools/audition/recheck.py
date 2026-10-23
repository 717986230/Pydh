import json, os, unicodedata
BASE = os.path.dirname(os.path.abspath(__file__))
TEXT = "皮影戏里讲故事，史进大闹史家村，请师傅王进教枪棒。窗外黄鹂飞过长江，天色渐渐暗了下来。"
SUSPECTS = ["hubert","isabella","qvd_01522","vd2_r8_rep1k_0007_v068_28k_g5k","vd2_r82_rep5k_2279_v068_28k_g5k",
"vd2_r82_rep5k_0400_v068_28k_g5k","vd2_r82_rep5k_0573_v068_28k_g5k","vd2_r82_rep5k_2045_v068_28k_g5k",
"vd2_r82_rep5k_2694_v068_28k_g5k","vd2_r8_rep500_0063_v068_28k_g5k","vdc_22255","vdc_3944","vd2_r8_rep5k_3469_v068_28k_g5k"]
def clean(s): return "".join(ch for ch in s if unicodedata.category(ch).startswith("L"))
def cer(ref, hyp):
    r, h = clean(ref), clean(hyp)
    dp = list(range(len(h)+1))
    for i, rc in enumerate(r, 1):
        prev, dp[0] = dp[0], i
        for j, hc in enumerate(h, 1):
            cur = dp[j]; dp[j] = min(dp[j]+1, dp[j-1]+1, prev+(rc != hc)); prev = cur
    return dp[len(h)]/max(1,len(r))
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
out = {}
for slug in SUSPECTS:
    mp3 = os.path.join(BASE, f"{slug}.mp3")
    segs, info = model.transcribe(mp3, language="zh", beam_size=5)
    hyp = "".join(s.text for s in segs)
    out["avocado_v2:"+slug] = {"cer_small": round(cer(TEXT, hyp),3), "transcript_small": hyp}
    print(slug, round(cer(TEXT,hyp),3), "|", hyp[:70], flush=True)
json.dump(out, open(os.path.join(BASE,"recheck_small.json"),"w"), ensure_ascii=False, indent=1)
print("RECHECK DONE")
