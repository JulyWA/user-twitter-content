# 机会抓取知识库指南

更新时间：2026-05-15

这个仓库的主定位已经调整为：**套利 / 隐藏机会抓取与策略复刻知识库**。

它不再把 KOL 当成“项目投研评分标准”，也不再默认服务于 BTCdayu + 0xSunNFT 双体系打分。旧的投研画像可以保留为辅助资料，但主工作流是：

1. 发现别人公开分享的套利、对冲、资金费率、价差、积分、早期隐藏机会。
2. 归档原文和截图。
3. 拆出收益来源、交易腿、监控字段、风险条件。
4. 判断能否复刻、改造或开发成自己的策略。
5. 沉淀成可执行的监控系统和策略研究笔记。

## 优先使用的数据

| 文件 | 用途 |
|---|---|
| `docs/ARBITRAGE_STRATEGY_DIGEST.md` | 套利策略专题入口 |
| `data/index/arbitrage_strategies.jsonl` | 所有套利/对冲/价差/资金费率相关记录 |
| `data/index/arbitrage_visual_strategies.jsonl` | 带图或截图的套利策略记录，优先用于复刻监控面板 |
| `data/index/twitter_knowledge_all.jsonl` | 跨 KOL 的完整知识层 |
| `data/users/<handle>/knowledge/report.md` | 单个 KOL 的机会画像 |
| `data/users/<handle>/knowledge/research_logic.md` | 单个 KOL 的策略复刻逻辑 |

## 当前主力 KOL 路由

| 需求 | 优先 KOL |
|---|---|
| Perp DEX、积分、现金流、Variational/Lighter/Backpack | Metabape |
| 期权套利、订单簿深度、严谨风控、错价监控 | yourQuantGuy |
| 高频套利工程、交易所 API、借贷机器人、失败复盘 | sunlc_crypto |
| 套保、止损、交易场所可靠性 | Vida_BWE |
| DeFi 协议收入、LP 风险、APR/TVL 质量 | Super4DeFi |
| 美股/AI 股票雷达和跨市场主线 | xiaomustock |

BTCdayu、0xSunNFT、bitfish、SonMa84176 仍可作为背景参考，但不再是默认评分体系。

## 机会记录的标准拆解

每条机会尽量拆成下面这些字段：

| 字段 | 说明 |
|---|---|
| opportunity_type | funding / basis / spread / options / points / airdrop / lending / monitor |
| source_kol | 来源 KOL |
| source_url | 原文链接 |
| has_media | 是否有截图或图表 |
| venues | 涉及交易所、协议、链 |
| instruments | 涉及币种、合约、股票、期权 |
| long_leg | 多头/现货/存款/质押腿 |
| short_leg | 空头/合约/对冲腿 |
| yield_source | 收益来源 |
| cost_source | 成本来源 |
| required_monitoring | 需要监控的字段 |
| execution_steps | 可复刻步骤 |
| risk_triggers | 风险触发条件 |
| automation_potential | 是否适合自动化 |
| status | 可复刻 / 需研究 / 已过期 / 高风险排除 |

## 复刻前检查

### 1. 收益来源

- funding / basis / spread / option mispricing / points / lending APR 哪一个是真正收益？
- 是否有多重收益叠加？
- 空投或积分是否只是 bonus？

### 2. 可执行性

- 当前是否还有价差或费率？
- 订单簿深度是否足够？
- 资金进出是否顺畅？
- 是否有地区、KYC、账户、税务或 API 限制？

### 3. 风险

- 单边行情是否会爆仓？
- 对冲腿是否完全匹配？
- 现货是否可借？
- 交易所是否暂停提币？
- 协议规则是否可能修改？
- 公开后收益是否已经收敛？

### 4. 监控字段

Crypto 套利至少监控：

- price_a / price_b
- spread %
- funding_a / funding_b
- implied APR / realized APR
- orderbook depth
- max executable size
- margin ratio
- liquidation price
- borrow availability
- deposit / withdrawal status
- net APY after fee/slippage/funding

带图记录优先从 `arbitrage_visual_strategies.jsonl` 里找。

## 输出格式

做一个机会研究时，建议输出：

```md
# 机会名称

## 快速结论

- 状态：可复刻 / 需研究 / 已过期 / 高风险排除
- 机会类型：
- 来源 KOL：
- 原文链接：
- 是否有截图：

## 策略结构

- 收益来源：
- 多头腿：
- 空头腿：
- 成本：
- 预期收益：

## 监控字段

| 字段 | 来源 | 阈值 | 用途 |
|---|---|---|---|

## 风险条件

-

## 复刻步骤

1.
2.
3.

## 自动化潜力

- 是否适合脚本监控：
- 是否适合自动执行：
- 最小可行版本：

## 需要人工复核

-
```

## 禁止事项

- 不要把 KOL 分享过的收益当作当前仍可获得的收益。
- 不要把带图推文当作完整策略文档，必须重新拆字段。
- 不要忽略手续费、滑点、税务、提现限制和 API 失败。
- 不要把旧“双体系打分”结论作为是否执行套利策略的依据。
- 不要提交 API key、cookie、token、真实账户和仓位数据。
