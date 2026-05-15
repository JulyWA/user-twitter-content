# sunlc_crypto 知识报告

## 数据卡

- Handle：[@sunlc_crypto](https://x.com/sunlc_crypto)
- 认证状态：蓝 V / `verified_or_above=true`
- 粉丝数：38,621
- 已归档推文：741 条
- 入库知识记录：220 条
- 套利相关记录：49 条
- 带图套利记录：26 条
- 核心价值：高频套利框架、交易所 API、借贷机器人、反撸复盘、资金费率风险。

## 一句话画像

sunlc_crypto 更像“工程化套利和踩坑复盘”的样本。他会写机器人、API、交易所开发，也会直接指出资金费率套利里现货借光、盘前合约收割、反撸项目这类风险。

## 可复刻方向

| 方向 | 可复刻字段 | 代表证据 |
|---|---|---|
| 高频套利框架 | 交易所连接、Rust、11 个交易所、AI 辅助开发 | https://x.com/sunlc_crypto/status/2029881612243194116 |
| 借贷机器人 | Bitfinex 借贷利率、闲置资金、年化收益 | https://x.com/sunlc_crypto/status/1722062729459179982 |
| 价差高频套利 | 妖币、价差、资金费率陷阱、现货可借数量 | https://x.com/sunlc_crypto/status/1703319879749951504 |
| 反撸项目复盘 | Blast、Blur、BP、资金成本、反撸概率 | https://x.com/sunlc_crypto/status/1788026374256808303 |
| ZEC 暂停提币价差 | 提币暂停、价差定价、止损、亏损复盘 | https://x.com/sunlc_crypto/status/1911724694811943113 |
| Lighter API 评估 | API 质量、对冲策略、开发成本 | https://x.com/sunlc_crypto/status/1912421602064740723 |

## 最值得看的带图记录

- 高频套利框架升级到 Rust：https://x.com/sunlc_crypto/status/2029881612243194116
- Bitfinex 借贷机器人和交易所套利：https://x.com/sunlc_crypto/status/1722062729459179982
- 高频价差套利和资金费率陷阱：https://x.com/sunlc_crypto/status/1703319879749951504
- ZEC 价差套利失败复盘：https://x.com/sunlc_crypto/status/1911724694811943113
- Lighter API 对冲策略评估：https://x.com/sunlc_crypto/status/1912421602064740723

## 策略复刻 checklist

1. 先判断是价差、资金费率、借贷利率、空投/反撸还是 API 工程机会。
2. 检查现货是否可借，避免 funding 套利被庄家提前锁死现货。
3. 对暂停提币、跨所充提、链拥堵做异常状态处理。
4. 机器人必须监控交易所 API、盘口、成交、借贷利率和异常延迟。
5. 对反撸项目计算 USDT 资金成本，而不是只看积分。
6. 对高频策略优先做风控、日志和熔断。

## 风险提醒

- 他公开的失败复盘很有价值，尤其适合提炼“不要做什么”。
- 高频套利工程复杂度高，API 质量和异常状态比策略本身更容易出问题。
- 资金费率套利不是无脑套，现货借光和庄家控盘会让新手接盘。
