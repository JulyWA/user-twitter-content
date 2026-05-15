# yourQuantGuy 套利逻辑沉淀

## 核心模型

yourQuantGuy 的套利模型可以概括为：**先证明结构可套利，再证明规模可成交，最后证明极端行情下不会死。**

## 重要信号矩阵

| 信号 | 观察方式 | 为什么重要 | 证据链接 |
|---|---|---|---|
| 订单簿深度 | 截图中 bid/ask 量、可成交规模 | 决定价差是否能实际套利 | https://x.com/yourQuantGuy/status/1989985886503674229 |
| implied vs realized APR | Boros/商品/TradFi funding 的预期和实际收益 | 判断收益是否被高估 | https://x.com/yourQuantGuy/status/2037180469033275590 |
| 期权四腿结构 | long/short put/call、strike、expiry、premium | 用结构锁定低风险收益 | https://x.com/yourQuantGuy/status/1937554377868210500 |
| 杠杆倍数 | 中性策略单边爆仓风险 | 方向中性不代表保证金中性 | https://x.com/yourQuantGuy/status/1955485878446420260 |
| 监控触发 | 错价期权、价差、资金费率异常 | 决定能否第一时间行动 | https://x.com/yourQuantGuy/status/2027757580357861791 |

## 否决信号

| 否决信号 | 动作 |
|---|---|
| 价差存在但深度太薄 | 限制规模或放弃 |
| 收敛时间不可控 | 加入资金时间成本 |
| 税务/账户摩擦吞掉收益 | 重算净收益 |
| 杠杆导致单边爆仓 | 降杠杆或拆仓位 |
| 无法自动监控错价 | 不把策略当稳定收益来源 |

## 可复刻监控字段

- instrument
- venue_a / venue_b
- bid / ask
- executable spread
- depth at size
- implied APR
- realized APR
- margin usage
- liquidation distance
- option legs
- max profit / max loss
- tax/friction estimate
- alert threshold

## 使用流程

1. 先把策略写成结构图：哪条腿赚钱、哪条腿对冲。
2. 用订单簿验证可成交规模。
3. 用极端行情验证保证金安全。
4. 扣掉费用、税务、资金时间成本。
5. 做自动监控，不靠手动刷屏。
6. 公开机会默认衰减，持续更新阈值。
