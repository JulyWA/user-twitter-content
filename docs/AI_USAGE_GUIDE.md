# AI 使用指引

更新时间：2026-05-14

这份文档写给团队成员，以及团队成员使用的其他 AI。目标是让任何人或 AI 拿到这个 public repo 后，可以直接基于已经归档和筛选过的内容做分析，而不是重复抓取、误读数据或把噪音当结论。

## 一句话说明

这是一个 KOL 机会知识库，不是简单的推文备份，也不是项目打分器。仓库里已经包含：

- 每个 KOL 的 Twitter/X 抓取结果。
- 规则筛选后的知识记录。
- 每个 KOL 的中文报告和投研逻辑。
- 跨 KOL 的全局索引。
- 套利/隐藏机会专题索引和带图策略索引。

如果只是做分析，通常不需要再次调用 RapidAPI。

## 推荐阅读顺序

### 第一步：了解全局结构

先读：

1. `README.md`
2. `docs/OPPORTUNITY_CAPTURE_GUIDE.md`
3. `docs/ARBITRAGE_STRATEGY_DIGEST.md`
4. `docs/KOL_KNOWLEDGE_DIGEST.md`

这些文件回答：

- 当前有哪些 KOL。
- 每个人适合抓取什么机会。
- 每个人的核心信号和否决信号是什么。
- 哪些 KOL 适合做策略复刻、监控面板或风险复盘。

### 第二步：查看单个 KOL

每个 KOL 目录下优先读：

```text
data/users/<handle>/knowledge/report.md
data/users/<handle>/knowledge/research_logic.md
```

`report.md` 适合快速理解这个账号能提供什么机会线索。

`research_logic.md` 适合提取策略复刻 checklist、监控字段和风险过滤规则。

### 第三步：需要机器分析时读 JSONL

如果要让 AI 批量检索、聚类、做 RAG 或专题研究，优先使用：

```text
data/index/twitter_knowledge_all.jsonl
data/index/twitter_links_all.jsonl
data/index/users.json
```

如果只分析某个 KOL，使用：

```text
data/users/<handle>/knowledge/twitter_knowledge.jsonl
data/users/<handle>/knowledge/twitter_links.jsonl
data/users/<handle>/sources/twitter/normalized/tweets.jsonl
```

## 文件用途说明

| 文件 | 用途 | 是否推荐给 AI 优先读取 |
|---|---|---|
| `docs/OPPORTUNITY_CAPTURE_GUIDE.md` | 机会抓取和策略复刻主工作流 | 是 |
| `docs/ARBITRAGE_STRATEGY_DIGEST.md` | 套利策略专题摘要 | 是 |
| `docs/KOL_KNOWLEDGE_DIGEST.md` | 全局摘要，说明每个 KOL 的价值和主题 | 是 |
| `docs/KOL_BACKGROUND_REFERENCE.md` | 历史投研背景参考，当前作为辅助资料 | 视任务需要 |
| `docs/KOL_DOC_FORMAT.md` | 单个 KOL 报告和逻辑文档的格式规范 | 是，尤其是要新增报告时 |
| `data/index/users.json` | 用户列表、数据量、认证状态、类别分布 | 是 |
| `data/index/twitter_knowledge_all.jsonl` | 跨 KOL 入库知识记录合集 | 是 |
| `data/index/twitter_links_all.jsonl` | 跨 KOL 链接保留记录合集 | 视任务需要 |
| `data/index/arbitrage_strategies.jsonl` | 跨 KOL 套利策略记录合集 | 做套利研究时优先 |
| `data/index/arbitrage_visual_strategies.jsonl` | 带图/截图的套利策略记录合集 | 想复刻监控面板时优先 |
| `data/users/<handle>/knowledge/report.md` | 单个 KOL 的人类可读报告 | 是 |
| `data/users/<handle>/knowledge/research_logic.md` | 单个 KOL 的信号、否决、流程、问题库 | 是 |
| `data/users/<handle>/knowledge/twitter_knowledge.jsonl` | 单个 KOL 的知识记录 | 是 |
| `data/users/<handle>/sources/twitter/normalized/tweets.jsonl` | 已抓取的标准化推文文本 | 需要全文检索时使用 |
| `data/users/<handle>/knowledge/twitter_excluded.jsonl` | 被规则排除的噪音样本 | 调筛选规则时使用 |

## JSONL 字段说明

### `twitter_knowledge.jsonl`

每行是一条进入知识库的推文记录，常用字段：

```json
{
  "source": "twitter",
  "username": "BTCdayu",
  "tweet_id": "...",
  "url": "https://x.com/.../status/...",
  "created_at": "...",
  "categories": ["project_thesis", "market_cycle"],
  "score": 10,
  "text": "...",
  "quoted_text": "...",
  "metrics": {
    "views": 12345,
    "likes": 100,
    "retweets": 10,
    "replies": 5,
    "quotes": 2
  },
  "filter_reasons": ["project_thesis:AI,收入"]
}
```

AI 使用时应优先关注：

- `username`
- `url`
- `created_at`
- `categories`
- `score`
- `text`
- `quoted_text`
- `filter_reasons`

### `users.json`

每个用户一条记录，包含：

- handle
- profile
- 是否蓝 V / verified_or_above
- 推文数量
- 入库知识数量
- 链接记录数量
- 时间范围
- 主要类别分布

AI 在选择数据源时，应先读取 `users.json` 判断每个账号适合什么任务。

## 推荐分析方式

### 做机会/套利策略研究

建议流程：

1. 优先在 `arbitrage_strategies.jsonl` 搜索项目名、ticker、交易所、协议、策略关键词。
2. 如果需要截图或面板字段，优先用 `arbitrage_visual_strategies.jsonl`。
3. 对每条结论保留原文 `url`。
4. 区分观点类型：
   - funding / basis
   - spread / orderbook
   - options
   - points / airdrop
   - lending / borrow
   - monitor / alert
   - 风险提醒
5. 用 `OPPORTUNITY_CAPTURE_GUIDE.md` 的字段拆解策略结构。
6. 输出结论时明确写出“来源 KOL、原文链接、可复刻性、监控字段、风险条件”。

### 做 KOL 画像

建议流程：

1. 先读该 KOL 的 `report.md`。
2. 再读 `research_logic.md`。
3. 用 `twitter_knowledge.jsonl` 抽样验证。
4. 如果账号 RT 占比较高，区分原创和转推。
5. 输出画像时避免只写标签，要写“可用场景”和“不能单独使用的场景”。

### 做写作风格参考

建议流程：

1. 不要直接模仿单条推文。
2. 先从 `report.md` 的写作风格部分理解结构。
3. 再从 `twitter_knowledge.jsonl` 找高分样本。
4. 只参考表达结构，不复制原文句子。
5. 输出时使用自己的观点和材料。

## 重要使用原则

### 不要重复抓取

如果任务只是分析、总结、检索、生成报告，不要调用 RapidAPI。

只有在以下情况才需要重新抓取：

- 新增 KOL。
- 更新已有 KOL 的最新内容。
- 需要补抓 replies、pinned 或 search endpoint。
- 当前数据明显缺失。

### 不要提交 key

任何 AI 或团队成员都不应该提交：

- `.env.local`
- RapidAPI key
- GitHub token
- cookie
- session
- 私密来源数据

### 不要把当前数据称为官方全量

当前数据是 RapidAPI 当前可分页窗口内的归档，不等于 X 官方意义上的全历史全量。

正确表述：

> 已归档当前接口可抓取窗口内的推文。

不要表述为：

> 已抓取账号注册以来所有推文。

### 不要把 RT 当成本人观点

如果 `text` 以 `RT @` 开头，说明它是转推。使用时应：

- 追溯原作者。
- 不把结论直接归因给当前 KOL。
- 可以把它视为“该 KOL 关注的信号源”。

### 所有结论要保留证据链接

输出分析时，每个关键结论都应尽量附上：

- KOL handle
- 原文 URL
- 简短解释

例子：

```text
0xSunNFT 对 Meme 周期更重视“龙头/龙二”和“明确催化”，证据见：
https://x.com/0xSunNFT/status/...
```

## 给其他 AI 的系统提示模板

可以把下面这段贴给其他 AI：

```text
你正在使用一个 KOL 知识库 repo。请优先读取 README.md、docs/OPPORTUNITY_CAPTURE_GUIDE.md、docs/ARBITRAGE_STRATEGY_DIGEST.md、docs/KOL_KNOWLEDGE_DIGEST.md、data/index/users.json。

如果需要分析具体 KOL，请读取 data/users/<handle>/knowledge/report.md 和 research_logic.md。

如果需要机器检索，请使用 data/index/twitter_knowledge_all.jsonl，并保留每条记录的 url 作为证据。

不要重复调用 Twitter/RapidAPI，除非任务明确要求更新抓取。
不要提交或索要任何 API key、GitHub token、cookie。
不要把当前数据称为账号注册以来的官方全量；只能称为当前接口可抓取窗口内的归档。
如果推文 text 以 RT @ 开头，不要直接归因为当前 KOL 原创观点。
请用中文输出，结论必须说明来源、适用场景和需要人工复核的地方。
```

## 常见任务模板

### 任务：分析某个项目

给 AI 的任务可以这样写：

```text
请基于这个 repo 的 KOL 机会知识库，分析 <项目名/ticker/策略关键词> 是否存在可复刻套利或隐藏机会。
先在 data/index/arbitrage_strategies.jsonl 和 data/index/arbitrage_visual_strategies.jsonl 检索相关记录，再结合 docs/OPPORTUNITY_CAPTURE_GUIDE.md 拆解策略结构。
输出：
1. 相关 KOL 和原文链接
2. 收益来源
3. 交易腿/对冲腿
4. 需要监控的字段
5. 风险/否决信号
6. 可复刻性判断
7. 下一步研究问题清单
```

### 任务：生成某个 KOL 的画像

```text
请读取 data/users/<handle>/knowledge/report.md、research_logic.md、twitter_knowledge.jsonl。
输出这个 KOL 的：
1. 核心研究视角
2. 最重要信号
3. 否决信号
4. 适合用来分析什么项目
5. 不适合单独参考的场景
6. 5 条原文证据链接
```

### 任务：比较多个 KOL

```text
请比较 <handle1>、<handle2>、<handle3> 在 <主题> 上的判断差异。
优先读取各自的 research_logic.md，再检索 twitter_knowledge.jsonl。
输出表格：
KOL / 核心观点 / 支持证据链接 / 风险提醒 / 如何组合使用。
```

## 当前最适合的 KOL 路由

| 任务 | 优先 KOL |
|---|---|
| 美股交易主线、AI 股票、ETF/期权 | xiaomustock |
| 长期产业链、估值、AI 基建价值投资 | BTCdayu |
| Meme、链上交易、事件驱动、空投 | 0xSunNFT |
| 风险管理、仓位和时间尺度 | bitfish |
| DeFi 协议收入、LP 风险、TVL/APR | Super4DeFi |
| BTC/山寨结构风险、杠杆清算、上币异常 | SonMa84176 |
| 交易执行、止损、套保、CEX/DEX Perp 比较 | Vida_BWE |
| 套利策略、资金费率、价差、带图监控复刻 | Metabape / yourQuantGuy / sunlc_crypto |

## 维护建议

新增或更新 KOL 后，应同步更新：

1. `data/index/users.json`
2. `docs/KOL_KNOWLEDGE_DIGEST.md`
3. `docs/KOL_BACKGROUND_REFERENCE.md`
4. 该 KOL 的 `report.md`
5. 该 KOL 的 `research_logic.md`

新增 KOL 的文档格式应遵守：

```text
docs/KOL_DOC_FORMAT.md
```
