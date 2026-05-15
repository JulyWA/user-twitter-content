# sunlc_crypto 套利逻辑沉淀

## 核心模型

sunlc_crypto 的套利模型可以概括为：**套利不是看到 APY 就上，而是工程、风控、异常状态和资金成本的系统战。**

## 重要信号矩阵

| 信号 | 观察方式 | 为什么重要 | 证据链接 |
|---|---|---|---|
| API 质量 | 交易所 API 是否稳定、设计是否合理 | 决定能否自动化执行 | https://x.com/sunlc_crypto/status/1912421602064740723 |
| 高频框架 | 交易所连接数量、语言、延迟、风控 | 决定策略规模和稳定性 | https://x.com/sunlc_crypto/status/2029881612243194116 |
| 现货可借量 | 资金费率套利前现货是否被借光 | 决定能否真实对冲 | https://x.com/sunlc_crypto/status/1703319879749951504 |
| 充提状态 | 暂停提币、开放时间、跨所价差 | 价差可能是风险定价，不是免费钱 | https://x.com/sunlc_crypto/status/1911724694811943113 |
| 资金成本 | USDT 利率、套保成本、积分稀释 | 反撸项目常输给资金成本 | https://x.com/sunlc_crypto/status/1788026374256808303 |

## 否决信号

| 否决信号 | 动作 |
|---|---|
| 现货已被借光 | 不做资金费率套利 |
| 提币暂停导致价差扩大 | 视为风险定价，谨慎止损 |
| API 难用或不稳定 | 不做自动化对冲 |
| 积分收益跑不赢资金成本 | 放弃反撸 |
| 无日志和熔断 | 不上高频策略 |

## 可复刻监控字段

- exchange status
- websocket latency
- orderbook spread
- borrow availability
- lending APR
- funding APR
- deposit/withdraw status
- chain congestion
- API error rate
- position mismatch
- realized PnL
- strategy kill switch

## 使用流程

1. 先看机会类型：价差、费率、借贷、反撸、API。
2. 检查是否能真实对冲：现货、借币、充提、链状态。
3. 计算资金成本和异常状态损失。
4. 做最小可行机器人：行情、交易、风控、日志、熔断。
5. 小资金跑稳定后再扩容。
6. 失败复盘进入黑名单规则。
