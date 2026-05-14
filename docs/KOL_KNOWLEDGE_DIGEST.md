# KOL 知识库摘要

更新时间：2026-05-14

这份文档是 JSONL 数据之上的“人类可读层”。它不堆原始推文，而是说明：这批数据抓到了什么、哪些内容有价值、以后可以怎么用于项目研究和内容写作。

## 当前覆盖范围

| KOL | 已归档推文 | 入库知识记录 | 仅保留链接记录 | 主要价值 |
|---|---:|---:|---:|---|
| BTCdayu | 829 | 268 | 190 | 价值投资、AI 基建、稳定币/Circle、市场周期风险、长文研报线索 |
| 0xSunNFT | 782 | 367 | 251 | 链上交易、Meme 周期、CEX 上币逻辑、事件驱动交易、空投/撸毛机制 |
| xiaomustock | 798 | 275 | 331 | AI 二级市场、产业链主线、股票/期权仓位、链上 Perp 叙事 |
| bitfish | 736 | 200 | 171 | 风险管理、仓位和时间尺度、稳定币/交易所基础设施、周期认知 |
| Super4DeFi | 837 | 179 | 74 | DeFi 协议收入、链上流动性、LP 风险、发行机制、回购分红 |
| SonMa84176 | 615 | 155 | 237 | BTC/宏观风险、杠杆清算、做市筹码、上币异常、散户陷阱 |
| Vida_BWE | 335 | 99 | 38 | Prop trading 风控、套保、CEX/DEX Perp 对比、交易复盘 |

跨 KOL 索引文件：

- `data/index/users.json`
- `data/index/twitter_knowledge_all.jsonl`
- `data/index/twitter_links_all.jsonl`
- `docs/KOL_DOC_FORMAT.md`：账号报告和投研逻辑文档的固定格式

## 文档层级

每个 KOL 的中文文档分两层：

| 文件 | 作用 | 使用方式 |
|---|---|---|
| `report.md` | 账号级知识报告，说明这个账号有什么价值、适合什么场景、有哪些证据链接 | 初次了解一个 KOL 时先读 |
| `research_logic.md` | 投研逻辑沉淀，包含重要信号矩阵、否决信号矩阵、使用流程和问题库 | 做项目研究 checklist 时使用 |

新增 KOL 的文档已经升级为“可审计版本”：核心判断都尽量挂原文链接，并标注 RT/转推使用提醒。

## 这批内容到底有什么用

### 1. 提炼项目研究逻辑

知识层保留的不是“所有推文”，而是可复用的判断框架、项目研究片段、风险信号和表达样本。

BTCdayu 适合用来：

- 判断一个资产是否有真实业务质量：收入、护城河、管理层、行业趋势、估值空间。
- 研究 AI 基建价值链：算力、电力、存储、光互联、HBM、芯片。
- 用商业模式和市场结构视角分析 Circle/USDC/稳定币。
- 识别币圈 PVP 结构：VC、项目方、交易所、KOL 轮、解锁压力、散户接盘。

0xSunNFT 适合用来：

- 理解链上交易员如何判断催化、流动性、CEX 上币路径和叙事强度。
- 提炼 Meme 周期玩法：龙头 vs 跟涨、事件驱动、流动性时机、退出信号。
- 学习真实交易复盘：买什么、卖什么、为什么、错在哪里、边际优势是什么。
- 研究空投/撸毛机会：规则、激励、预期收益、时间成本和机会成本。

xiaomustock 适合用来：

- 从公开市场角度识别长期主线，例如 AI 数据中心、存储、光互联、白银、航天。
- 判断一个赛道里谁接近利润池，谁只是资本开支重、护城河弱的苦生意。
- 参考股票、ETF、期权和 crypto 叙事之间的跨市场表达。

bitfish 适合用来：

- 建立风险管理和仓位纪律：可控变量、时间尺度、流动性、情绪。
- 分析稳定币、MSTR、交易所产品里的风险再分配机制。
- 把市场现象压缩成结构框架，而不是只做方向预测。

Super4DeFi 适合用来：

- 判断 DeFi 协议是否有真实收入和代币价值捕获。
- 分析 LP、TVL、APR、做市、资管和项目方之间的风险分配。
- 研究发行机制、回购分红和协议现金流。

SonMa84176 适合用来：

- 识别杠杆清算、做市不足、筹码失控和上币前异常钱包。
- 判断短线走势是否是散户陷阱或假突破。
- 把 BTC/山寨价格波动拆成宏观、杠杆、流动性和散户行为。

Vida_BWE 适合用来：

- 参考实盘交易复盘、观点证伪、动态止损和套保纪律。
- 对比 CEX/DEX Perp 在极端行情下的可靠性。
- 用可比估值判断高 FDV 项目是否过热。

### 2. 参考语言风格

BTCdayu 的表达风格：

- 偏长文、解释型、反思型。
- 常把一个市场案例上升为更大的投资原则。
- 喜欢用“错过/亏损/教训/认知升级”的方式讲投资逻辑。
- 适合参考来写项目研报、价值投资风格长推、行业分析。

0xSunNFT 的表达风格：

- 直接、战术化、交易后复盘感强。
- 常用“设置条件 -> 触发因素 -> 操作 -> 结果 -> 教训”的结构。
- 适合参考来写交易复盘、链上机会笔记、短中期行情判断。

新增五个账号的风格速写：

- xiaomustock：口语化交易笔记，强个人判断，适合写跨市场主线和二级仓位复盘。
- bitfish：克制、框架化、风险管理优先，适合写市场结构和交易纪律。
- Super4DeFi：DeFi 实务和社区流动性视角，适合写协议收入、LP 风险、代币价值捕获。
- SonMa84176：短线结构和风险提示强，适合写清算、上币异常、做市筹码。
- Vida_BWE：实盘交易员风格，强调证伪、止损、套保和交易基础设施风险。

### 3. 作为未来分析的源地图

当前数据已经足够支持：

- 为每个 KOL 生成投资框架总结。
- 建立项目级记忆，例如 `CRCL`、`HYPE`、`Hyperliquid`、`Based`、`Fartcoin`、`AI16Z`、`AIXBT`。
- 按类别查看内容：`project_thesis`、`market_cycle`、`onchain_strategy`、`risk_warning`、`research_source`。
- 提取写作风格样本，用于未来生成你自己的内容。

## 高价值主题

### BTCdayu

| 主题 | 为什么重要 | 去哪里看 |
|---|---|---|
| AI 基建 | 高频讨论算力、存储、HBM、光互联、基础设施瓶颈，适合做 AI 基建投研。 | `data/users/BTCdayu/knowledge/twitter_knowledge.jsonl` |
| 稳定币/Circle | 多条内容涉及 Circle/USDC、收入逻辑、分成、估值，适合稳定币和支付基础设施分析。 | 搜索 `Circle`、`CRCL`、`USDC` |
| 币圈 PVP 结构 | 对 VC、项目方、交易所、散户接盘结构有明确批判，适合做风险框架。 | 类别 `market_cycle`、`risk_warning` |
| Pre-IPO / 公开市场交叉 | 涉及 SpaceX、字节、Cerebras、RKLB、HBM、AI 硬件、港股 IPO。 | 搜索 `IPO`、`Cerebras`、`SpaceX`、`RKLB` |
| 亏损教训 | 可提炼风控清单：少幻想、留现金、Meme 小仓位、赚到后及时兑现。 | `risk_warning` 记录 |

代表链接：

- 币圈 PVP 市场结构：https://x.com/BTCdayu/status/2022112193794408548
- 风险教训、现金、Meme 仓位：https://x.com/BTCdayu/status/2015656975712022786
- Circle / CRCL 建仓和估值思路：https://x.com/BTCdayu/status/2034122263889645822
- Hyperliquid / HYPE 解锁和团队行为：https://x.com/BTCdayu/status/2039560077540217309
- AI 基建 / HBM 价值链：在 `twitter_knowledge.jsonl` 搜索 `HBM`

### 0xSunNFT

| 主题 | 为什么重要 | 去哪里看 |
|---|---|---|
| 链上交易打法 | 有大量关于 LP、流动性、杠杆、代币机制、交易复盘的记录。 | 类别 `onchain_strategy`、`asset_reference` |
| Meme 龙头/跟涨逻辑 | 明确区分真龙头、跟涨反弹、接盘陷阱。 | 搜索 `Fartcoin`、`Trump`、`Goat`、`Chillguy` |
| CEX 上币和代币发行 | 适合分析上币压力、FDV、筹码分配、解锁、流动性。 | 搜索 `CEX`、`Binance`、`Coinbase`、`FDV` |
| 空投/撸毛 | 包含 Blast、Lighter、TradeXYZ、Based、Hyperliquid 生态机会。 | 搜索 `Blast`、`Lighter`、`Based`、`Hyperliquid` |
| 事件驱动交易 | 明确框架：方向性 + 波动性；当市场注意力聚合时，新闻会产生可交易机会。 | 搜索 `新闻交易`、`事件驱动` |

代表链接：

- Memeland / MEME 操作复盘：https://x.com/0xSunNFT/status/1720482602111660526
- Meme 做空选标逻辑：https://x.com/0xSunNFT/status/1930722585828118705
- Tron Meme 周期和龙头依赖：https://x.com/0xSunNFT/status/1826868036978311401
- HYPE 交易复盘：https://x.com/0xSunNFT/status/2018558780968243621
- Blast 规则研究：https://x.com/0xSunNFT/status/1727217431830290939

### 新增五个账号速览

| KOL | 最值得沉淀的逻辑 | 代表链接 |
|---|---|---|
| xiaomustock | 长期主线、利润池位置、交易工具降风险 | https://x.com/xiaomustock/status/2050459686785155338 |
| bitfish | 仓位、时间尺度、流动性、风险收益交换 | https://x.com/bitfish/status/2023039775293452628 |
| Super4DeFi | 协议收入、LP 风险、回购分红、发行机制 | https://x.com/Super4DeFi/status/1888077065079111745 |
| SonMa84176 | 杠杆清算、项目拉盘条件、上币异常 | https://x.com/SonMa84176/status/2000876489794052211 |
| Vida_BWE | 观点证伪、动态止损、套保、交易场所可靠性 | https://x.com/Vida_BWE/status/2017171924661534787 |

## 如何用于项目研究

研究一个新项目时，可以按这个顺序用知识库：

1. 在全局索引里搜索项目名、ticker、链、赛道关键词。
2. 把匹配记录分成几类：
   - 投资 thesis
   - 风险信号
   - 市场时机
   - 可比项目
   - 交易/撸毛玩法
3. 对比两个 KOL 的视角：
   - BTCdayu 视角：业务质量、长期趋势、估值、护城河、现金流、管理层。
   - 0xSunNFT 视角：催化、流动性、龙头地位、CEX 路径、聪明钱、时机、抛压。
4. 最后整理成项目研究 memo：
   - 这个资产是什么？
   - 为什么现在值得看？
   - 边际买家是谁？
   - 最大风险是什么？
   - 什么条件会改变判断？

## 当前盲点

- Twitter API 返回的是可分页窗口，不一定是账号注册以来的真正全历史。
- Telegram 和公众号内容还没有进入知识库。
- 现在是规则筛选，不是完美语义筛选，仍需要人工抽查。
- 报告是摘要层，完整文本仍在 JSONL 里，方便机器分析。

## 推荐下一步

下一步可以按主题生成专题页，而不是继续只堆数据：

- `topics/ai_infra.md`
- `topics/stablecoin_circle.md`
- `topics/hyperliquid_hype.md`
- `topics/meme_cycle.md`
- `topics/pre_ipo.md`

这些专题页应该跨 KOL 综合观点，输出“可直接用于项目研究”的结论。
