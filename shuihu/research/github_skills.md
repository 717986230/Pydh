# GitHub Skills / 工具调研：水浒皮影批量流水线可借鉴项

调研日期：2026-10-23。方法：GitHub 连接器查元数据 + 逐仓读 README/SKILL.md/LICENSE 原文核实，未只凭标题推荐。星标与更新时间截至调研当日。本次仅调研，未安装、未克隆、未运行任何代码。

## 我们的流水线现状（对照基线）
AI 生成镜头 → 中文 TTS 旁白 → Python+ffmpeg 合成（烧录字幕、按旁白时长剪镜）→ QUEUE.md 批量队列（每轮 ≤6 镜）→ 抽帧自检 → 发布。主要可改进点：①字幕与旁白的时间对齐靠估算；②字幕断行靠字数硬切（≤18 字）；③批量生产无缓存/幂等，返工要整段重跑；④分镜与 QC 没有标准化模板与检查表。

## Top 3 推荐

### 1. blazerior/videoediting-claude-skill — 借它的「批量流水线架构」
- URL：https://github.com/blazerior/videoediting-claude-skill ｜ 星标：2（新仓，2026-10 更新）｜ 许可证：MIT（已读 LICENSE 原文）
- 已读内容：SKILL.md + references/batch-pipeline.md。其结构：SKILL.md 只放流程与铁律，细节拆到 references（pipeline / storyboard / batch-pipeline / ffmpeg-cookbook / troubleshooting「17 个各花了一小时调试的故障」）。
- 对我们的改进：其 `pipeline.py` 分阶段（ingest→transcribe→probe→subs→base→final→qa）、**按输入哈希缓存、每阶段幂等、重跑零成本**、project.json 清单与生成物分离、最后出一张全批 QA 联系表（contact strip）统一验片——正好把我们 QUEUE.md 的「记账式队列」升级为「缓存式流水线」，返工只重跑受影响的镜/阶段；troubleshooting 与 cookbook 可直接充实我们的优化日志。
- 注意：它面向「实拍素材+口播转写」剪辑，字幕走 faster-whisper 转写路线，与我们「先有旁白文本」不同；借架构与脚本模式即可，不要整套照搬。仓库很小很新，脚本务必逐个审读后再用。

### 2. rany2/edge-tts — 用 TTS 自带时间戳根治字幕对齐
- URL：https://github.com/rany2/edge-tts ｜ 星标：12,357（2026-10-22 仍更新）｜ 许可证：MIT（已读 LICENSE 原文）
- 已读内容：README。edge-tts 调用微软 Edge 在线 TTS（免费、无需 key，含 zh-CN 神经音色），关键点是它能通过边界元数据（boundary metadata）**在合成时直接输出带精确时间的字幕（--write-subtitles 生成 SRT）**——字幕时机来自 TTS 本身，不需要再跑 ASR 猜时间。
- 对我们的改进：旁白逐段合成时同步拿到逐句/逐词时间戳，合成阶段按真实时间烧录字幕，消灭「按字数估时长」带来的漂移；这也是 MoneyPrinterTurbo 的字幕方案之一（见下条，edge 模式）。
- 注意：这是非官方接口，旁白文本会发往微软服务器；可用性与条款随微软策略变化，需留本地 TTS 兜底。

### 3. zenstory-ai/video-recap-skills — 借它的中文解说生产与 QC 规范
- URL：https://github.com/zenstory-ai/video-recap-skills ｜ 星标：588（2026-10-22 更新，0 open issues）｜ 许可证：MIT（README 许可证徽章指向其 LICENSE）
- 已读内容：README。7 个技能（6 生产 + 1 参考）：故事计划、声音分工、旁白、时间线、QC 报告、看片修改记录，全套产物在 examples/ 里有完整样例可对照；本地只需 ffmpeg。
- 对我们的改进：把我们 storyboard.md 从「分镜表」升级为带故事计划 + QC 报告 + 修改记录的标准件，正好服务「工作流不断优化」的要求；其看片-QC-返修闭环可直接写进 WORKFLOW 的自检步骤。
- 注意：它的 ASR/VLM/TTS 依赖小米 MiMo 的 API key（付费云端、内容出境），我们只需借其工作流与文档规范，不要引入这个 key 依赖；它的输入是现成视频做解说，与我们「AI 生成镜头」不同，借的是组织方法而非生成环节。

## 其余候选（按相关度排序）

### 4. harry0703/MoneyPrinterTurbo — 成熟的整机参考实现
- https://github.com/harry0703/MoneyPrinterTurbo ｜ 134,240 星（当日仍在更新）｜ MIT（第三方 2026-10 复核与仓库一致）
- 已读 README。要点：字幕两条路线（edge-TTS 时间戳 / faster-whisper）、逐词弹字幕样式、批量任务队列（≤100 条）、可喂本地素材（即能拿我们的生成镜头当素材）、下载与渲染并发可调。
- 用法建议：当「字幕时间戳生成 + 批量队列」的参考实现来读源码，不必整机部署（它的定位是主题→素材库口播片，与皮影叙事不合）。
- ⚠️ 安全/版权：其 `resource/songs` 默认 BGM 来源不清、多篇评测与 README 均提醒发布前删除——我们只用抖音曲库，不碰它的音乐；示例配置把 API 绑 0.0.0.0，若将来试跑必须改 127.0.0.1；config.toml 里集中放各家 API key，切勿进 git。

### 5. Huanshere/VideoLingo — 字幕语义断句的参考
- https://github.com/Huanshere/VideoLingo ｜ 18,888 星（2026-10-22 更新）｜ Apache-2.0（已读 LICENSE 原文）
- 已读 README。要点：NLP+AI 语义字幕切割（按语义断句而非字数）、词级对齐（WhisperX / Qwen3-ForcedAligner）、单行长度规范——正是我们「≤18 字硬切」规则的升级方向：旁白先语义断句再排字幕。
- 注意：本体是 Streamlit 重型应用（翻译/配音向、偏 GPU），借它的断句方法与提示词即可，不要整机引入。

### 6. linyqh/NarratoAI — 中文解说文案与剪辑提示词参考
- https://github.com/linyqh/NarratoAI ｜ 11,501 星（2026-10-22 更新）｜ MIT（已读 LICENSE 原文）
- 已读 README。LLM 写解说文案、按文案匹配镜头、配音字幕一站式。其解说文案提示词可作我们「脚本提示词」的对照样本；但它面向影视片段解说，与原创生成镜头匹配度一般，优先级低于上面几家。README 内含多个赞助推广链接，与功能无关，忽略即可。

### 7. Vincentwei1021/anything2explainer — 帧级时间线与 QC 方法
- https://github.com/Vincentwei1021/anything2explainer ｜ 2,685 星（2026-10-22 更新）｜ 许可证：本次未检出 LICENSE 原文，采用前必须先确认
- 已读 SKILL.md。要点：TTS 词边界 → 帧-accurate 时间线 + 字幕表；storyboard 源文件格式；frame_metrics 量化验帧；多 agent 分工与 QC 判据。画面是 Remotion 代码绘制，与皮影实拍式生成不合，但「时间线生成法 + QC 判据」值得抄作业。许可证未确认前只读方法、不复制代码。

### 8. calesthio/OpenMontage — 大型 agentic 生产系统（仅作架构参考）
- https://github.com/calesthio/OpenMontage ｜ 70,889 星（当日仍更新）｜ AGPLv3（README 许可证徽章）
- 已读 README。12 条生产流水线、数百个 skill/知识文件，零 key 可用 Piper TTS + ffmpeg 后期。体量与 AGPL 传染性都不适合我们的小流水线整机采用；当「别人怎么组织生产知识库」的样本翻一翻即可。

### 9. WyattBlue/auto-editor — 旁白停顿修剪（边际优化）
- https://github.com/WyattBlue/auto-editor ｜ 5,592 星（2026-10-22 更新）｜ Unlicense（据项目文档）
- 按响度自动剪静音段。我们是「旁白定时长驱动镜头」，偶尔可用它收紧 TTS 段间气口，收益边际。Nim 编写，若将来用只取官方 Release 二进制并核对校验和，不跑不明构建脚本。

### 10. Agentchengfeng/chengfeng-videocut-skills — 暂缓
- https://github.com/Agentchengfeng/chengfeng-videocut-skills ｜ 3,118 星（2026-10-22 更新）
- 已读 README：它只是插件入口，本体 Runtime 在另一仓；且 README 自承当前公开 Runtime v0.4.11 不满足新 Skill 的能力要求、缺能力时只能停。面向口播剪辑，版本钉死关系复杂，现阶段不值得引入。

### 11. dean9703111/ai-agent-skill-for-video-workflow — SRT 增强小技能
- https://github.com/dean9703111/ai-agent-skill-for-video-workflow ｜ 219 星
- audio-to-srt（OpenAI Whisper API）+ srt-enhancer（AI 语义重断句）。思路与 VideoLingo 的断句重叠且更轻，但依赖付费 Whisper API 且要上传音频，优先级低。

### 12. zhuyansen/awesome-claude-video-skills — 索引（发现渠道）
- https://github.com/zhuyansen/awesome-claude-video-skills ｜ 823 星（2026-10-22 更新）
- 约 180 个视频类 skill/工具仓的分类清单且带安全评级。不是工具本身，适合以后每轮优化时来这里找新候选（FireRed-OpenStoryline、OpenChatCut 等也在其列）。

## 通用安全须知（采用任何一家前）
- Agent skills 本质是「指令 + 脚本」，会以 agent 的权限执行；业内已出现恶意 skill 案例（LOLSkills 项目专门曝光此类仓库）。规矩：**钉死 commit 版本、逐个脚本审读后再运行、优先借鉴模式与提示词而非直接执行外来代码**，必要时用 lolskills.io 之类扫描器过一遍。
- 凡要求把 API key 写进仓库自带 config 模板的（如 MoneyPrinterTurbo、video-recap-skills 的 MiMo key），先确认 key 的发送目的地，配置文件绝不进 git、绝不进我们的工作目录模板。
- edge-tts 等「免费云端」能力意味着文本/音频出境到微软等第三方，属可用但需知情的取舍；成片发布仍按既有规则勾选抖音「内容由AI生成」。

## 一句话结论
先抄两样：videoediting-claude-skill 的**哈希缓存分阶段批量流水线**（升级 QUEUE）+ edge-tts 的**TTS 时间戳字幕**（根治对齐）；再把 video-recap-skills 的**QC 闭环**写进 WORKFLOW。其余作为参考库按需查阅。
