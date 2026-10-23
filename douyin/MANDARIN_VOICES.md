# 普通话配音白名单（选角唯一依据 · 2026-10-23 建）

> 背景：配音音色库不标注方言，部分音色念中文会滑粤语、甚至只会拼音式朗读。选角只能从本名单的「已验证」里挑；名单外音色必须先过试音门（tools/audition：同一段普通话标准句合成 → Whisper 转写逐字比对，base+small 双模型；错字率 ≤0.40 且转写为简体连贯普通话才算合格）。

## 已验证 · 普通话（可直接选角）
男声：
- avocado_v2:MAI_03（温和男声 · 旁白/刘备）
- avocado_v2:magnus（深沉威严 · 关羽/王进）
- avocado_v2:vd2_r8_rep1k_0104_v068_28k_g5k（极低沙哑 · 张飞）
- avocado_v2:vd2_exacting_pillar（中文深沉持重 · 崂山道士）
- avocado_v2:vd2_r82_rep5k_0654_v068_28k_g5k（中文爽朗 · 陈达）
- avocado_v2:vd2_r82_rep5k_0686_v068_28k_g5k（中文明亮诚恳）
- avocado_v2:vd2_r82_rep5k_2875_v068_28k_g5k（儒雅中年 · 林如海）
- avocado_v2:qvd_00052（高亮活泼 · 贾宝玉）
- avocado_v2:qvd_01498（中音明亮 · 客乙）
- avocado_v2:qvd_01879（清朗睿智）
- avocado_v2:qvd_02166（高音鼻音 · 千里眼）
- avocado_v2:qvd_02220（深沉愉悦 · 客甲）
- avocado_v2:qvd_02331（中音睿智）
- avocado_v2:qvd_02823（明亮高音 · 王生）
- avocado_v2:ronan（亲切随和）
女声：
- avocado_v2:melody（自信爽利 · 王熙凤）
- avocado_v2:vd2_brittle_fan（中文高音轻盈 · 林黛玉）
- avocado_v2:qvd_02303（轻柔 · 嫦娥/王夫人）
- avocado_v2:qvd_02863（中音亲切 · 探春）
- avocado_v2:qvd_03766（中音温柔 · 王生妻/贾母）
- avocado_v2:vd2_r82_rep5k_2555_v068_28k_g5k（极高飘逸 · 丫鬟甲）
- avocado_v2:vg_tt_f49（欢快丰润 · 邢夫人）
- avocado_v2:MAI_01（温暖亲切 · 李纨）
- avocado_v2:qvd_01406（低音温柔 · 迎春）
- avocado_v2:vdc_11859（高音明亮 · 惜春）
- avocado_v2:rumi（活泼明亮 · 备用女声）
- avocado_v2:marisol（爽利温暖 · 备用女声）
- avocado_v2:qvd_03187（深亮女声 · 备用）

## 不合格 · 禁用（试音实测）
粤语读法（转写繁体化、系统性粤语读音）：
- avocado_v2:hubert（原张飞）、avocado_v2:isabella（原王夫人）、avocado_v2:qvd_01522（原千里眼）、avocado_v2:vd2_r8_rep1k_0007_v068_28k_g5k（原迎春）、avocado_v2:vd2_r8_rep5k_3469_v068_28k_g5k（原林黛玉）、avocado_v2:vd2_r82_rep5k_2279_v068_28k_g5k、avocado_v2:qvd_04170（批次2）
不支持中文（拼音式朗读/乱码）：
- avocado_v2:vdc_22255（原崂山道士）、avocado_v2:vdc_3944（原陈达）、avocado_v2:vd2_r8_rep500_0063_v068_28k_g5k（原客甲）、avocado_v2:vd2_r82_rep5k_0400_v068_28k_g5k（原贾宝玉）、avocado_v2:vd2_r82_rep5k_0573_v068_28k_g5k（原李纨）、avocado_v2:vd2_r82_rep5k_2045_v068_28k_g5k（原惜春）、avocado_v2:vd2_r82_rep5k_2694_v068_28k_g5k（原贾母）、avocado_v2:vdc_5、avocado_v2:vdc_6534、avocado_v2:vdc_16748、avocado_v2:vdc_27524（批次2）；avocado_v2:Vanessa 中文不合格（仅限英文内容使用）
