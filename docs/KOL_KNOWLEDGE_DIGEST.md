# KOL Knowledge Digest

Last built: 2026-05-14

This digest is the human-readable layer above the JSONL files. It explains what was captured, what is useful, and how the material can support project research or content writing.

## Current Coverage

| KOL | Twitter records | Knowledge records | Link-only records | Main value |
|---|---:|---:|---:|---|
| BTCdayu | 829 | 268 | 190 | Value investing, AI infrastructure, stablecoin/Circle, market-cycle risk, long-form research references |
| 0xSunNFT | 782 | 367 | 251 | On-chain trading, meme cycles, CEX listing logic, event-driven trades, airdrop/farming mechanics |

Cross-user indexes:

- `data/index/users.json`
- `data/index/twitter_knowledge_all.jsonl`
- `data/index/twitter_links_all.jsonl`

## What Is Actually Useful Here

### 1. Project Research Logic

The knowledge layer captures reusable reasoning patterns rather than only tweet text.

BTCdayu is useful for:

- Evaluating whether an asset has real business quality: revenue, moat, management, industry trend, valuation room.
- Thinking about AI infrastructure as a multi-layer value chain: compute, power, storage, optical interconnect, memory, chips.
- Looking at Circle/USDC and stablecoins through business-model and market-structure lenses.
- Detecting crypto PVP structures: VC, project teams, exchanges, KOL rounds, unlock pressure, retail exit liquidity.

0xSunNFT is useful for:

- Understanding how on-chain traders judge catalysts, liquidity, CEX listing paths, and narrative strength.
- Extracting meme-cycle playbooks: leader vs follower, event-driven momentum, liquidity timing, and when to exit.
- Studying actual trade retrospectives: what was bought/sold/shorted, why, and what mistake or edge mattered.
- Understanding airdrop/farming strategy from rules, incentives, expected value, and opportunity cost.

### 2. Style Reference

BTCdayu style:

- Long-form, explanatory, reflective.
- Often turns market examples into broader principles.
- Uses analogies and regret/lesson framing to make investment points memorable.
- Good reference for writing project research threads or value-investing-style notes.

0xSunNFT style:

- Direct, tactical, post-trade, detail-heavy.
- Often explains setup, trigger, position logic, risk, and retrospective in one flow.
- Good reference for writing trade recaps, on-chain opportunity notes, and short-to-mid-term market judgement.

### 3. Source Map For Future Analysis

The current dataset already gives enough material to build:

- Per-KOL investment framework summaries.
- Project-specific memory, for example `CRCL`, `HYPE`, `Hyperliquid`, `Based`, `Fartcoin`, `AI16Z`, `AIXBT`.
- Category-level views: `project_thesis`, `market_cycle`, `onchain_strategy`, `risk_warning`, `research_source`.
- Writing-style samples for future content generation.

## High-Value Themes Found

### BTCdayu

| Theme | Why it matters | Where to look |
|---|---|---|
| AI infrastructure | Repeated focus on compute, storage, HBM, optical interconnect, and infra bottlenecks. Useful for AI-infra project research. | `data/users/BTCdayu/knowledge/twitter_knowledge.jsonl` |
| Stablecoin/Circle | Multiple records around Circle/USDC, revenue logic, fee sharing, and valuation. Useful for stablecoin and payment-infra analysis. | Search `Circle`, `CRCL`, `USDC` |
| Crypto market structure | Strong material on why crypto becomes PVP, why many token structures hurt retail, and why BTC is treated differently. | Categories `market_cycle`, `risk_warning` |
| Pre-IPO / public market crossover | Mentions SpaceX, ByteDance, Cerebras, RKLB, HBM, AI hardware, and Hong Kong IPO context. Useful beyond crypto. | Search `IPO`, `Cerebras`, `SpaceX`, `RKLB` |
| Lessons from losses | Reusable risk checklist: do not over-fantasize, keep cash, size meme positions small, take profit after lucky gains. | `risk_warning` records |

Representative links:

- PVP market structure: https://x.com/BTCdayu/status/2022112193794408548
- Risk lessons / cash / meme sizing: https://x.com/BTCdayu/status/2015656975712022786
- Circle / CRCL positioning and valuation thinking: https://x.com/BTCdayu/status/2034122263889645822
- Hyperliquid/HYPE unlock and team behavior: https://x.com/BTCdayu/status/2039560077540217309
- AI infrastructure and HBM chain: search `HBM` in `twitter_knowledge.jsonl`

### 0xSunNFT

| Theme | Why it matters | Where to look |
|---|---|---|
| On-chain playbooks | Detailed records of setups, LP construction, leverage, token mechanics, and post-trade accounting. | Categories `onchain_strategy`, `asset_reference` |
| Meme leader/follower logic | Strong distinction between true leader, follower rebound, and exit-liquidity traps. | Search `Fartcoin`, `Trump`, `Goat`, `Chillguy` |
| CEX listing and token launch | Useful material on listing pressure, FDV, allocation, unlocks, and liquidity. | Search `CEX`, `Binance`, `Coinbase`, `FDV` |
| Airdrop/farming | Practical records on Blast, Lighter, TradeXYZ, Based, and Hyperliquid ecosystem opportunities. | Search `Blast`, `Lighter`, `Based`, `Hyperliquid` |
| Event-driven trading | Explicit framework: direction plus volatility; news creates tradable moves when market attention converges. | Search `新闻交易`, `事件驱动` |

Representative links:

- Memeland/MEME operation recap: https://x.com/0xSunNFT/status/1720482602111660526
- Meme short-selection logic: https://x.com/0xSunNFT/status/1930722585828118705
- Tron meme cycle and leader dependence: https://x.com/0xSunNFT/status/1826868036978311401
- HYPE trade retrospective: https://x.com/0xSunNFT/status/2018558780968243621
- Blast rule research: https://x.com/0xSunNFT/status/1727217431830290939

## How To Use This In Project Research

For a new project, use the knowledge base in this order:

1. Search the global index for project name, ticker, chain, and sector.
2. Read matching KOL records and separate them into:
   - thesis
   - risk warning
   - market timing
   - comparable projects
   - trade/farming playbook
3. Compare KOL lenses:
   - BTCdayu lens: business quality, durability, valuation, moat, cash flow, management, secular trend.
   - 0xSunNFT lens: catalyst, liquidity, leader status, CEX path, smart money, timing, exit pressure.
4. Turn matches into a structured research memo:
   - What is the asset?
   - Why now?
   - Who is the marginal buyer?
   - What can go wrong?
   - What would change the view?

## Current Blind Spots

- The Twitter API window may not be true historical all-time coverage.
- Telegram and WeChat sources are not yet ingested.
- Rule-based filtering is useful but not perfect; some records still need manual review.
- The reports are summaries, while the full text remains in JSONL for machine analysis.

## Recommended Next Step

Build project/topic pages from the indexed records:

- `topics/ai_infra.md`
- `topics/stablecoin_circle.md`
- `topics/hyperliquid_hype.md`
- `topics/meme_cycle.md`
- `topics/pre_ipo.md`

These pages should synthesize across KOLs instead of storing raw posts.
