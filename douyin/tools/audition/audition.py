import json, os, subprocess, sys, unicodedata
BASE = os.path.dirname(os.path.abspath(__file__))
TEXT = "皮影戏里讲故事，史进大闹史家村，请师傅王进教枪棒。窗外黄鹂飞过长江，天色渐渐暗了下来。"
CANTONESE_MARKERS = list("嘅咗唔係乜嘢點樣嚟畀佢哋冇睇諗")
VOICES = ["avocado_v2:MAI_03","avocado_v2:hubert","avocado_v2:isabella","avocado_v2:magnus","avocado_v2:melody",
"avocado_v2:qvd_00052","avocado_v2:qvd_01498","avocado_v2:qvd_01522","avocado_v2:qvd_01879","avocado_v2:qvd_02166",
"avocado_v2:qvd_02220","avocado_v2:qvd_02303","avocado_v2:qvd_02331","avocado_v2:qvd_02823","avocado_v2:qvd_02863",
"avocado_v2:qvd_03766","avocado_v2:ronan","avocado_v2:vd2_r82_rep5k_0400_v068_28k_g5k","avocado_v2:vd2_r82_rep5k_0573_v068_28k_g5k",
"avocado_v2:vd2_r82_rep5k_2045_v068_28k_g5k","avocado_v2:vd2_r82_rep5k_2555_v068_28k_g5k","avocado_v2:vd2_r82_rep5k_2694_v068_28k_g5k",
"avocado_v2:vd2_r8_rep1k_0007_v068_28k_g5k","avocado_v2:vd2_r8_rep500_0063_v068_28k_g5k","avocado_v2:vd2_r8_rep5k_2875_v068_28k_g5k",
"avocado_v2:vd2_r8_rep5k_3469_v068_28k_g5k","avocado_v2:vdc_22255","avocado_v2:vdc_3944","avocado_v2:vg_tt_f49",
"avocado_v2:vd2_brittle_fan","avocado_v2:vd2_exacting_pillar","avocado_v2:vd2_r8_rep1k_0104_v068_28k_g5k",
"avocado_v2:vd2_r82_rep5k_0654_v068_28k_g5k","avocado_v2:vd2_r82_rep5k_0686_v068_28k_g5k","avocado_v2:vd2_r82_rep5k_2279_v068_28k_g5k","avocado_v2:MAI_01","avocado_v2:warm_concat_0305","avocado_v2:warm_mai01_en","avocado_v2:warm_short_0305","avocado_v2:rumi","avocado_v2:marisol","avocado_v2:Vanessa","avocado_v2:vdc_5","avocado_v2:vdc_11859","avocado_v2:vdc_6534","avocado_v2:vdc_16748","avocado_v2:vdc_27524","avocado_v2:vdc_NOID66","avocado_v2:qvd_01406","avocado_v2:qvd_03187","avocado_v2:qvd_04170"]
def clean(s):
    return "".join(ch for ch in s if unicodedata.category(ch).startswith("L"))
def cer(ref, hyp):
    r, h = clean(ref), clean(hyp)
    if not r: return 1.0
    dp = list(range(len(h)+1))
    for i, rc in enumerate(r, 1):
        prev, dp[0] = dp[0], i
        for j, hc in enumerate(h, 1):
            cur = dp[j]
            dp[j] = min(dp[j]+1, dp[j-1]+1, prev+(rc != hc))
            prev = cur
    return dp[len(h)] / len(r)
def main():
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    results = {}
    done_file = os.path.join(BASE, "audition_results.json")
    if os.path.exists(done_file):
        results = json.load(open(done_file))
    for vid in VOICES:
        if vid in results: continue
        slug = vid.split(":",1)[1]
        mp3 = os.path.join(BASE, f"{slug}.mp3")
        if not os.path.exists(mp3):
            p = subprocess.run(["/opt/hatch/bin/tts","speak","--output",mp3,"--language","zh","--voice",vid,"--text-stdin"],
                               input=TEXT.encode(), capture_output=True)
            if p.returncode != 0 or not os.path.exists(mp3) or os.path.getsize(mp3)==0:
                results[vid] = {"error": "tts failed"}; continue
        segs, info = model.transcribe(mp3, language="zh", beam_size=5)
        hyp = "".join(s.text for s in segs)
        markers = sorted({c for c in hyp if c in CANTONESE_MARKERS})
        e = cer(TEXT, hyp)
        verdict = "PASS" if (e <= 0.25 and not markers) else "FAIL"
        results[vid] = {"cer": round(e,3), "cantonese_markers": markers, "transcript": hyp, "verdict": verdict}
        print(vid, verdict, "cer", round(e,3), "markers", markers, flush=True)
        json.dump(results, open(done_file,"w"), ensure_ascii=False, indent=1)
    print("DONE", sum(1 for v in results.values() if v.get("verdict")=="PASS"), "pass /", len(results))
if __name__ == "__main__":
    main()
