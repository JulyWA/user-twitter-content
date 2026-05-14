# KOL Knowledge Base Design

目标不是保存所有社交媒体噪音，而是沉淀每个信息源的研究逻辑、项目判断、表达风格和可追溯原文。

## 第一阶段范围

优先处理 KOL 的 Twitter/X 内容：

```text
data/users/<handle>/
  profile.json
  sources/
    twitter/
      raw/tweets_raw.json
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

后续可以把 `<handle>` 扩展为更通用的实体 ID，例如：

- `kol/<handle>`
- `fund/<org>`
- `research_site/<site>`
- `investor/<person>`

当前先保持简单：每个 Twitter handle 一个目录。

## 三层数据

### 1. Raw

原始 API 返回。用于追溯、重跑筛选、修复字段。

建议不要提交到 public repo，除非你确认体积、版权和隐私风险都可接受。

### 2. Normalized

稳定字段的一行一条 JSONL，适合脚本分析和后续喂给模型。

### 3. Knowledge

真正进入知识库的内容：

- 项目 thesis
- 投资框架和筛选标准
- 市场周期判断
- 链上交易逻辑
- 风险信号
- 仓位和交易计划
- 有复用价值的表达风格样本

## 排除原则

默认不进入知识库：

- 纯生活、天气、情绪、寒暄
- 抽奖、无上下文转发
- 只有表情或短句
- 无判断、无事实、无框架的信息

但如果这类内容带有重要链接，会进入 `twitter_links.jsonl`，只保留链接和上下文摘要，方便以后查原文。

## 筛选策略

`scripts/build_twitter_knowledge.py` 当前使用透明规则打分：

- 命中项目/估值/收入/TVL/解锁等词：提高分
- 命中框架/复盘/赔率/仓位等词：提高分
- 命中风险/砸盘/出货/清算等词：提高分
- 出现 cashtag 或合约地址：提高分
- 长文和高互动：适度加分
- 生活、抽奖、寒暄：降低分

这是第一层粗筛，不追求完美。后续可以再加 LLM 二次筛选：

- 摘要该条推文的可复用观点
- 标注项目、赛道、资产 ticker
- 抽取“判断依据 -> 结论 -> 触发条件”
- 建立每个 KOL 的语言风格样本库
