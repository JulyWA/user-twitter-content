# User Twitter Content

个人 KOL 知识库的第一阶段：抓取 Twitter/X 内容，按用户归档，并把真正有研究价值的内容筛入 knowledge 层。

目标不是“保存所有推文”，而是沉淀：

- 每个 KOL 的项目研究逻辑
- 投资框架、市场判断、风险偏好
- 有价值的原文链接
- 可参考的表达风格样本

## Key 写入模板

推荐只写到本机环境变量或 `.env.local`，不要提交 token。

临时写入当前终端：

```bash
export RAPIDAPI_KEY='替换成你的 RapidAPI key'
export RAPIDAPI_HOST='twitter241.p.rapidapi.com'
```

写入本仓库本地配置文件：

```bash
cp .env.example .env.local
# 然后手动把 .env.local 里的 replace_with_your_rapidapi_key 替换成真实 key
```

加载 `.env.local`：

```bash
set -a
source .env.local
set +a
```

抓取脚本也会默认自动读取仓库根目录的 `.env.local`；上面的 `source` 适合你想在同一个终端里连续跑多个命令的情况。

`.gitignore` 已经排除了 `.env.local`。

## 目录结构

每个账号一个文件夹，以 Twitter handle 命名：

```text
data/users/<handle>/
  sources/
    twitter/
      raw/tweets_raw.json
      raw/profile_raw.json
      normalized/profile.json
      normalized/tweets.jsonl
      clean/tweets_clean.json
    telegram/
      raw/
    wechat/
      raw/
  knowledge/
    twitter_knowledge.jsonl
    twitter_links.jsonl
    twitter_excluded.jsonl
    twitter_summary.md
  state/
    twitter_checkpoint.json
```

当前先实现 Twitter/X。Telegram 公开页和公众号归档先预留目录。

## 先看什么

如果你只是想知道这批内容有什么价值，优先看：

- `docs/AI_USAGE_GUIDE.md`：给团队成员和其他 AI 的使用指引，说明如何分析、如何引用证据、什么情况下不要重复抓取
- `docs/KOL_KNOWLEDGE_DIGEST.md`：全局摘要，说明每个 KOL 的可用价值和代表主题
- `docs/KOL_RESEARCH_LOGIC.md`：跨 KOL 的投研逻辑沉淀，重点是信号、否决条件、适用场景
- `docs/KOL_DOC_FORMAT.md`：每个 KOL 的 `report.md` 和 `research_logic.md` 固定格式规范
- `data/users/BTCdayu/knowledge/report.md`：BTCdayu 可读报告
- `data/users/BTCdayu/knowledge/research_logic.md`：BTCdayu 的价值投资/项目质量判断框架
- `data/users/0xSunNFT/knowledge/report.md`：0xSunNFT 可读报告
- `data/users/0xSunNFT/knowledge/research_logic.md`：0xSunNFT 的 Meme 周期/链上交易信号框架
- `data/users/<handle>/knowledge/report.md`：每个新增 KOL 的中文可读报告
- `data/users/<handle>/knowledge/research_logic.md`：每个新增 KOL 的投研逻辑、重要信号和否决信号
- `data/index/users.json`：每个用户的数据规模、时间范围、类别分布

## 抓取推文

先复制 handle 列表：

```bash
cp config/handles.example.txt config/handles.txt
```

编辑 `config/handles.txt` 后运行：

```bash
python3 scripts/archive_twitter_kols.py --user-file config/handles.txt
```

脚本默认使用你当前可用的 `Twttr API`：

```text
Host: twitter241.p.rapidapi.com
User lookup: GET /user?username=<handle>
User tweets: GET /user-tweets?user=<rest_id>&count=20&cursor=<cursor>
```

旧的 `The Old Bird / twitter154` 如果额度用完会返回 `HTTP 429`，当前不建议作为默认抓取源。

脚本会同时保存 `normalized/profile.json`，其中包含粉丝数、简介、`verified`、`is_blue_verified`、`verified_or_above` 等字段。新增 KOL 搜索和归档时，优先使用蓝 V / verified_or_above 账号。

小样本测试：

```bash
python3 scripts/archive_twitter_kols.py BTCdayu --max-pages 3
```

抓回复和置顶：

```bash
python3 scripts/archive_twitter_kols.py BTCdayu --include-replies --include-pinned
```

从第一页重新抓，但和本地已有数据去重合并：

```bash
python3 scripts/archive_twitter_kols.py BTCdayu --fresh
```

## 生成知识库

抓取后运行：

```bash
python3 scripts/build_twitter_knowledge.py
python3 scripts/build_index.py
```

只处理某几个用户：

```bash
python3 scripts/build_twitter_knowledge.py BTCdayu 0xSunNFT
```

调高筛选门槛：

```bash
python3 scripts/build_twitter_knowledge.py --threshold 8
python3 scripts/build_index.py
```

输出说明：

- `twitter_knowledge.jsonl`：进入知识库的推文
- `twitter_links.jsonl`：内容本身不够强，但值得保留的链接
- `twitter_excluded.jsonl`：被排除的噪音样本，方便以后调规则
- `twitter_summary.md`：数量统计

全局索引输出：

- `data/index/users.json`：每个用户的数据规模、时间范围、类别分布
- `data/index/twitter_knowledge_all.jsonl`：跨 KOL 的知识记录合集
- `data/index/twitter_links_all.jsonl`：跨 KOL 的链接合集

## 更新流程

后续新增或更新 KOL 时，标准顺序是：

```bash
python3 scripts/archive_twitter_kols.py --user-file config/handles.txt --sleep 3
python3 scripts/build_twitter_knowledge.py
python3 scripts/build_index.py
```

## Public Repo 提交建议

这个仓库是 public，建议提交：

- `scripts/`
- `docs/`
- `config/handles.example.txt`
- `.env.example`
- curated 后的 `knowledge/` 文件

谨慎提交：

- `sources/twitter/raw/`
- `state/`
- 任何包含 token、cookie、私密来源、未确认授权的大体量原始数据

当前 `.gitignore` 默认排除了 raw 和 state。

## GitHub 远程仓库

你创建的 public repo：

```bash
git init
git remote add origin https://github.com/JulyWA/user-twitter-content.git
git branch -M main
git add README.md .gitignore .env.example config docs scripts
git commit -m "Initialize KOL knowledge base"
git push -u origin main
```

## 重要限制

RapidAPI 的 timeline endpoint 能持续翻页直到 continuation token 消失，但这不等于官方意义上的历史全量搜索。它返回的是该 API 当前可分页窗口内的数据。

如果某个 KOL 只能抓到最近一段时间，后续需要增加 search endpoint，用类似 `from:handle since:YYYY-MM-DD until:YYYY-MM-DD` 的方式分段回补。

## 给团队成员和其他 AI

如果团队成员或他们使用的 AI 只需要分析知识库，不需要重新抓取，请优先阅读：

```text
docs/AI_USAGE_GUIDE.md
```

核心原则：

- 不要重复调用 RapidAPI，除非任务明确要求更新抓取。
- 不要提交 `.env.local`、API key、GitHub token、cookie。
- 不要把当前数据称为账号注册以来的官方全量。
- 分析结论要保留 KOL handle 和原文 URL。
- `RT @` 开头的内容不要直接归因为当前 KOL 原创观点。
