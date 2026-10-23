# 皮影短剧生产区 · 隔离规则
每部名著一个独立文件夹，互不混用：
- shuihu/（水浒传）、liaozhai/（聊斋志异）
- 每部有自己的 WORKFLOW、PROMPT_GUIDE、characters、SCENES、CONTINUITY、QUEUE、corpus、production。
- 通用经验（如提示词工艺）以誊抄方式同步到各部自己的文件，之后各自演进，不共用同一份文件，避免改一部坏另一部。
- 续产任务按季读取对应文件夹，只在接档时确认上一季 QUEUE 顶部状态，不跨季读写生产文件。
