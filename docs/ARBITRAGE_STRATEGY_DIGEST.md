# 套利策略知识库摘要

更新时间：2026-05-15

这份文档聚焦 KOL 公开分享的套利、对冲、价差、资金费率、积分挖矿和可复刻监控思路。它不是交易建议，而是把公开案例整理成“可复盘、可改造、可二次开发”的策略线索。

## 当前覆盖

| KOL | 已归档推文 | 入库知识 | 套利记录 | 带图套利记录 | 主要价值 |
|---|---:|---:|---:|---:|---|
| Metabape | 806 | 365 | 97 | 42 | Perp DEX、Lighter/Variational/Backpack、跨所套利、积分与现金流结合 |
| yourQuantGuy | 446 | 243 | 110 | 61 | 期权套利、Perp DEX、资金费率、订单簿深度、风险/杠杆管理 |
| sunlc_crypto | 741 | 220 | 49 | 26 | 高频套利框架、借贷机器人、资金费率风险、反撸复盘、API/工程实现 |

机器可读索引：

- `data/index/arbitrage_strategies.jsonl`：所有套利相关记录
- `data/index/arbitrage_visual_strategies.jsonl`：带图/截图的套利记录

## 三个 KOL 怎么分工

| 用途 | 优先看谁 | 原因 |
|---|---|---|
| 找 Perp DEX / 积分 / 现金流结合玩法 | Metabape | 案例多，常写“怎么做、收益来自哪里、监控什么” |
| 找严谨套利结构和风险解释 | yourQuantGuy | 有传统金融和量化背景，讲订单簿、杠杆、期权结构更清楚 |
| 找工程化监控和反例 | sunlc_crypto | 更关注机器人、API、失败复盘和“套利小白别踩坑” |

## 可复刻策略主题

### 1. Perp DEX 资金费率 / 价差套利

关注字段：

- 交易所 A / B 的 perp 价格和标记价格
- 现货价格或指数价格
- funding rate / implied APR / realized APR
- 订单簿深度
- 保证金占用
- 爆仓价格
- 对冲腿是否完全抵消
- 积分或空投收益是否能覆盖资金成本

代表证据：

- Metabape：Variational / Lighter 多种套利姿势和跨所收益：https://x.com/Metabape/status/1991944885021356513
- Metabape：SIGN 资金费率差异，币安 -2000% APY vs Variational 低费率：https://x.com/Metabape/status/1918233449984606318
- yourQuantGuy：价差套利里订单簿深度的重要性：https://x.com/yourQuantGuy/status/1989985886503674229
- sunlc_crypto：高频套利 1% 价差来回做，但提醒资金费套利可能被庄家反杀：https://x.com/sunlc_crypto/status/1703319879749951504

### 2. 积分 / 空投 + 对冲套利

关注字段：

- 交易量积分规则
- 保证金或存款积分权重
- OI / volume / borrow / lend 是否计分
- 套保成本
- funding 成本
- 空投预期价值
- 规则变更风险
- 反撸概率

代表证据：

- Metabape：Backpack 三季积分和 basis trading 复盘：https://x.com/Metabape/status/1989302487460000189
- Metabape：Virtuals 质押 + 合约开空套保 + genesis 交易量：https://x.com/Metabape/status/1928091299418362212
- yourQuantGuy：GRVT 保证金被动收入 + 反向完全对冲：https://x.com/yourQuantGuy/status/2008494866171392345
- sunlc_crypto：质押/刷单/反撸项目复盘，提醒资金成本和反撸风险：https://x.com/sunlc_crypto/status/1788026374256808303

### 3. 美股 / 期权 / 交易所美股合约套利

关注字段：

- 期权四腿结构
- 到期日
- 行权价
- 开仓价格
- 最大盈利 / 最大亏损
- 税务或账户摩擦
- 美股账户和 crypto 合约账户之间的资金调度

代表证据：

- yourQuantGuy：META 期权 iron condor 无风险套利结构：https://x.com/yourQuantGuy/status/1937554377868210500
- yourQuantGuy：META 期权套利仓位更新：https://x.com/yourQuantGuy/status/2016891218689507804
- yourQuantGuy：Lighter 美股合约和美股账户套利，但税务摩擦影响收益：https://x.com/yourQuantGuy/status/1993698031640727656

### 4. 机器人 / 监控面板

关注字段：

- 交易所连接状态
- ticker / funding / orderbook websocket
- 价差阈值
- 深度阈值
- 仓位阈值
- 保证金阈值
- 爆仓距离
- 借贷利率
- 自动告警
- 手动确认或自动执行

代表证据：

- sunlc_crypto：用 AI 升级高频套利框架到 Rust，完成 11 个交易所开发：https://x.com/sunlc_crypto/status/2029881612243194116
- sunlc_crypto：借贷机器人在 Bitfinex 吃利息：https://x.com/sunlc_crypto/status/1722062729459179982
- Metabape：用 OKX 钱包内置浏览器移动端监控 Variational 套利仓位：https://x.com/Metabape/status/1981715030849810465
- yourQuantGuy：如果自己做了监控，可以捕捉错价期权套利：https://x.com/yourQuantGuy/status/2027757580357861791

## 可复刻监控面板字段

结合带图推文和你补充的 Bewin Quant 风格截图，后续可以设计两类面板。

### Crypto 套利面板

- Pair / symbol
- 交易所 A price
- 交易所 B price
- spot / index price
- spread %
- funding rate A / B
- implied APR
- realized APR
- orderbook depth
- max executable size
- margin used
- liquidation price
- hedge mismatch
- borrow / lend rate
- points earned
- estimated airdrop value
- net APY after fee/funding/slippage
- alert reason

### 美股 / AI 股票雷达面板

- sector / sub-sector
- ticker
- price
- 1D / 5D / 1M / YTD return
- volume anomaly
- news catalyst
- valuation score
- growth score
- profitability score
- risk score
- AI exposure
- momentum
- analyst / earnings date
- watchlist tag
- alert reason

## 使用提醒

- 所有套利案例都必须复核实时价格、深度、手续费、税务和交易所限制。
- KOL 公开分享时，机会可能已经收敛。
- 带图推文适合复刻字段和监控逻辑，不代表可以复刻收益。
- RT 或引用内容要追溯原作者。
- 公开策略适合做启发，更适合在此基础上优化阈值、风控和执行系统。
