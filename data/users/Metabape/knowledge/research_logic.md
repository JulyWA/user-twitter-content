# Metabape 套利逻辑沉淀

## 核心模型

Metabape 的套利模型可以概括为：**先找现金流，再叠加积分；先确保仓位活着，再考虑空投赔率。**

## 重要信号矩阵

| 信号 | 观察方式 | 为什么重要 | 证据链接 |
|---|---|---|---|
| funding / basis 差异 | 不同交易所或合约之间 APY 差 | 直接决定现金流是否成立 | https://x.com/Metabape/status/1918233449984606318 |
| 积分规则 | 交易量、OI、保证金、质押是否计分 | 决定空投/积分收益是否可叠加 | https://x.com/Metabape/status/1989302487460000189 |
| 保证金安全 | 空单是否蚕食保证金，爆仓价如何变化 | 对冲完整也可能因保证金结构爆仓 | https://x.com/Metabape/status/1945130311895146543 |
| 盘口深度 | 哪个平台先动、哪个平台跟随 | 决定跨所套利能否成交 | https://x.com/Metabape/status/2050954376081297773 |
| 应急操作 | 移动端是否能存取款、加保证金 | 套利仓位常需要快速处理 | https://x.com/Metabape/status/1981715030849810465 |

## 否决信号

| 否决信号 | 动作 |
|---|---|
| APY 看起来高但深度不足 | 不下大仓位，先小额测试 |
| 对冲腿和保证金币种不匹配 | 重新计算爆仓路径 |
| 积分规则不透明或可能修改 | 只按现金流估值，空投作为 bonus |
| 需要频繁手动应急但无法移动端操作 | 降仓位或放弃 |

## 可复刻监控字段

- symbol
- exchange_a_price / exchange_b_price
- basis %
- funding APY
- orderbook depth
- position size
- margin ratio
- liquidation price
- points earned
- estimated point value
- net APY after fee/funding/slippage
- alert reason

## 使用流程

1. 先找现金流：funding、basis、负点差、亏损返还。
2. 再看积分：交易量、OI、质押、保证金是否加分。
3. 对每条腿分别计算费用、滑点、保证金和爆仓价。
4. 小额开仓测试，确认成交和监控有效。
5. 建仓后持续监控价差收敛、规则变化和保证金。
6. 机会公开扩散后，默认收益会快速下降。
