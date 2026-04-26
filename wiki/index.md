# LLM Knowledge Base — Index

> This index is maintained by Claude Code Agent. See [CLAUDE.md](../CLAUDE.md) for compile instructions.
> Manual notes go in the [Notes](#notes) section — they will not be overwritten.

---

<!-- AUTO-GENERATED -->

## Stats

| Metric | Count |
|--------|-------|
| Concept articles | 43 |
| Derived notes | 21 |
| Query records | 3 |
| Last compiled | 2026-04-23 |

---

## Concepts

> AI/LLM concepts extracted and synthesized from source material.

| Concept | One-line definition | Tags |
|---------|---------------------|------|
| [ACE Framework](concepts/ace-framework.md) | Three-role framework for LLM self-improvement via evolving playbooks | `agent`, `context-engineering`, `stanford`, `playbook` |
| [Hermes Agent Architecture](concepts/hermes-agent-architecture.md) | Nous Research's open-source closed-learning-loop agent with three-tier memory and self-extracting skills | `agent`, `self-improving`, `open-source`, `nous-research`, `FTS5` |
| [Context Engineering](concepts/context-engineering.md) | Systematic design and evolution of LLM context to improve behavior | `context-engineering`, `prompt-engineering`, `llm` |
| [Evolving Playbooks](concepts/evolving-playbooks.md) | Grow-and-Refine mechanism for accumulating strategies via delta updates | `playbook`, `delta-update`, `self-improving` |
| [Agentic Self-Improvement](concepts/agentic-self-improvement.md) | LLM agents improving task performance from experience without retraining | `agent`, `self-improving`, `meta-learning` |
| [Superapp Paradigm](concepts/superapp-paradigm.md) | Unified AI application consolidating chatbot, coding agent, and browser into one agentic surface | `superapp`, `ai-products`, `agentic-ai` |
| [API to SuperAgent Transition](concepts/api-to-superagent.md) | Shift from human-facing API integrations to agent-callable tool interfaces | `agentic-ai`, `mcp`, `superagent` |
| [Agent-Friendly Design](concepts/agent-friendly-design.md) | Design principles for software interfaces optimized for autonomous AI agent consumption | `mcp`, `tool-design`, `agent-friendly` |
| [Material Science Agents](concepts/material-science-agents.md) | LLM-based autonomous systems closing the hypothesis–experiment–analysis loop in materials research | `material-science`, `agent`, `closed-loop`, `multi-agent` |
| [ACE for Materials](concepts/ace-for-materials.md) | Application of ACE Generator/Reflector/Curator to materials discovery and scientific paper extraction | `material-science`, `ace-framework`, `closed-loop` |
| [Agent Evaluation](concepts/agent-evaluation.md) | Methods and benchmarks for evaluating multi-step autonomous agent performance | `agent`, `evaluation`, `benchmark`, `swe-bench`, `made` |
| [Agent Product Design](concepts/agent-product-design.md) | Design principles for building trustworthy agent products: autonomy spectrum, human-in-the-loop placement, trust building | `agent`, `product-design`, `human-in-the-loop`, `trust` |
| [Agentic Harness](concepts/agentic-harness.md) | Infrastructure surrounding an LLM loop (memory, compression, permissions, orchestration) that makes agents production-grade | `agent`, `harness`, `context-compression`, `permission-gating` |
| [Tiered Memory](concepts/tiered-memory.md) | Three-layer agent memory: always-loaded index (L1), on-demand topic files (L2), searchable transcripts (L3) | `agent`, `memory`, `context-engineering` |
| [Three-Tier Memory Systems](concepts/three-tier-memory-systems.md) | Comparative analysis of in-session compression (T1), FTS5 cross-session search (T2), and persistent MEMORY.md + skills (T3) | `agent`, `memory`, `FTS5`, `SQLite`, `hermes` |
| [Singapore Tech Career Strategy](concepts/singapore-tech-career-strategy.md) | Career and life-planning framework for SG PR holders in niche tech: HDB/CPF leverage, dual-base Taiwan–SG strategy, citizenship trade-offs | `career`, `singapore`, `PR`, `HDB`, `CPF`, `dual-base`, `career-resilience` |
| [Harness Engineering](concepts/harness-engineering.md) | Systematic discipline of guiding LLMs to their full potential via context, workflow, and feedback loop design — the broader framework containing Context Engineering and ACE | `harness-engineering`, `LLM`, `context-engineering`, `workflow`, `NTU`, `hung-yi-lee` |
| [Scaling Law Limitations](concepts/scaling-law-limitations.md) | Why Scaling Law is a "pessimistic future": diminishing returns on compute demand a paradigm shift toward RL, context engineering, and better guidance | `scaling-law`, `LLM`, `RL`, `efficiency`, `AGI`, `compute`, `FAIR` |
| [Technical-to-Business Transition](concepts/technical-to-business-transition.md) | Career framework for deep-tech ICs transitioning to VC/Strategy: 4-stage model, deal memo skill-building, 3-layer networking | `career`, `VC`, `strategy`, `transition`, `networking`, `deep-tech` |
| [Climbing Lock-Off Strength](concepts/climbing-lock-off-strength.md) | Static bent-arm strength — the biggest determinant of controlled reaches, near-universally asymmetric L/R | `climbing`, `lock-off`, `unilateral`, `training` |
| [Climbing Power Endurance](concepts/climbing-power-endurance.md) | Sustaining near-max contractions under pump — why link-ups fail even when single moves work | `climbing`, `power-endurance`, `pump`, `training` |
| [Climbing Compression Pulling](concepts/climbing-compression-pulling.md) | Bicep/pec-dominant inward pull — the Moonboard compression pattern pull-ups don't train | `climbing`, `compression`, `bicep`, `moonboard` |
| [RTK Token Killer](concepts/rtk-token-killer.md) | Rust CLI proxy that compresses shell output via PreToolUse hook, cutting 60–90% of tokens for Claude Code and 11 other agents | `agentic-harness`, `context-compression`, `claude-code`, `rust`, `cli-proxy` |
| [Local vs Cloud Coding Agents](concepts/local-vs-cloud-coding-agents.md) | Deployment-axis classification by shell execution locus — why RTK and other harness hooks apply only to local agents (Claude Code, Cursor) and not cloud ones (Devin, Codex) | `agent`, `deployment-model`, `devin`, `codex`, `hook-surface` |
| [CLI Output Compression](concepts/cli-output-compression.md) | Per-command filter/group/truncate/dedup of shell output before it enters LLM context; regex vs. structural-parsing approaches | `context-compression`, `agentic-harness`, `tooling`, `parsing` |
| [Information Theory for LLM Context](concepts/information-theory-for-llm-context.md) | Shannon entropy framing of why LLM-facing text is 80–95% redundant and where the practical compression ceiling sits | `information-theory`, `shannon`, `context-compression`, `entropy`, `economics` |
| [Claude Code Token Efficiency Playbook](concepts/claude-code-token-efficiency-playbook.md) | Boris Cherny's tips synthesised: effort levels, auto-compact window, worktrees, hooks, /simplify /batch, CLAUDE.md discipline | `claude-code`, `token-efficiency`, `bcherny`, `worktree`, `hooks`, `skills` |
| [Subagent Dispatch Economics](concepts/subagent-dispatch-economics.md) | Cost model for Claude Code's Agent/Task dispatch — when to inline, when to parallelise, when to bound thoroughness | `claude-code`, `subagent`, `dispatch`, `token-efficiency`, `bcherny` |
| [Mobile Dispatch Workflow](concepts/mobile-dispatch-workflow.md) | iPhone / remote Claude Code operating regime — no worktrees, no local hooks; Mac-launched long tasks + mobile check-in via /loop, /schedule, /btw | `claude-code`, `mobile`, `iphone`, `remote-development`, `dispatch`, `bcherny` |
| [Claude Managed Agents](concepts/claude-managed-agents.md) | Anthropic's managed-agent infrastructure — harness, memory store, cloud-hosted agent execution | `agent`, `infrastructure`, `harness`, `memory-store`, `anthropic`, `beta`, `cloud` |
| [Climbing Training System](concepts/climbing-training-system.md) | Parent framework for V4-V5 → V6-V7 climbing progression: periodisation, finger strength, injury prevention | `climbing`, `bouldering`, `training`, `finger-strength`, `periodization`, `personal` |
| [Memory Stores vs RAG](concepts/memory-stores-vs-rag.md) | Comparison of persistent memory stores and RAG for agent context — when to write vs. retrieve | `memory`, `rag`, `context-engineering`, `agent`, `comparison` |
| [RLPR (Reference Probability Reward)](concepts/rlpr-reference-probability-reward.md) | Extrapolating RLVR to general domains without verifiers via reference-model probability as reward | `RL`, `RLVR`, `reinforcement-learning`, `verifier-free`, `post-training` |
| [Cost-Aware Cascade Design](concepts/cost-aware-cascade-design.md) | Cheap-signal-→-threshold-→-escalate pattern generalised; threshold from cost minimisation; bottleneck rotates across product-lifecycle stages (POC→Alpha→Beta→GA→Mature) | `algorithm-design`, `cascade`, `cost-model`, `self-consistency`, `product-lifecycle`, `career`, `algorithm-engineer`, `triage` |
| [Self-Consistency Implementation](concepts/self-consistency-implementation.md) | Field-level aggregation + normalisation + numeric tolerance-band voting; per-field confidence is the real product, not the vote-winning value | `self-consistency`, `extraction`, `confidence`, `aggregation`, `implementation`, `patsnap`, `algorithm-engineer` |
| [LLM-as-Judge](concepts/llm-as-judge.md) | Stronger LLM scores/arbitrates weaker LLM's outputs; cheaper than self-consistency but inherits position/verbosity/self-preference biases | `evaluation`, `judge`, `pairwise`, `mt-bench`, `scoring`, `extraction`, `confidence` |
| [Verifier Model](concepts/verifier-model.md) | Small trained classifier predicting correctness — replaces LLM-as-Judge at scale once labelled data accumulates; OpenAI PRM lineage | `verifier`, `evaluation`, `classifier`, `process-reward-model`, `openai`, `extraction`, `cost-efficiency` |
| [Constrained Decoding](concepts/constrained-decoding.md) | Force schema-valid output at decode time (JSON Schema, tool use, Outlines); solves format correctness, not fact correctness | `structured-output`, `json-schema`, `tool-use`, `decoding`, `extraction`, `format-correctness` |
| [Retrieval-Augmented Verification](concepts/retrieval-augmented-verification.md) | Verify each extracted value is grounded in a source span; catches shared-prior hallucinations self-consistency reinforces | `hallucination`, `verification`, `citation`, `traceability`, `patent`, `extraction`, `rag` |
| [Self-Refine / Critic Loop](concepts/self-refine-critic-loop.md) | Same model generates → critiques → revises; works for reasoning/generation, marginal for atomic extraction | `self-refine`, `critic`, `iterative-improvement`, `reasoning`, `reflexion` |
| [Model Ensembling](concepts/model-ensembling.md) | Vote across Claude+GPT+Gemini to escape shared-prior errors; high engineering cost reserved for high-value low-volume tasks | `ensembling`, `robustness`, `cross-model`, `high-stakes`, `extraction`, `voting` |
| [Logprob Uncertainty](concepts/logprob-uncertainty.md) | Per-token logprobs as free confidence signal; OpenAI/self-hosted only — Anthropic Claude doesn't expose logprobs | `uncertainty`, `logprobs`, `calibration`, `confidence`, `extraction`, `openai` |
| [Active Learning Loop](concepts/active-learning-loop.md) | Low-confidence → human label → retrain/refresh; closes the feedback cycle around any confidence-aware pipeline | `active-learning`, `human-in-the-loop`, `drift`, `annotation`, `fine-tuning`, `snorkel`, `argilla` |

---

## Derived Notes

> Summaries of ingested source material (articles, papers, repos).

| Date | Title | Type | Key Concepts |
|------|-------|------|--------------|
| 2026-04-08 | [ACE: Agentic Context Engineering](derived/ace-agentic-context-engineering.md) | paper | ACE Framework, Evolving Playbooks |
| 2026-04-08 | [OpenAI Plans Desktop Superapp](derived/openai-superapp-superagent.md) | article | Superapp Paradigm, API to SuperAgent Transition, Agent-Friendly Design |
| 2026-04-08 | [ACE × Material Science Application](derived/ace-material-science-application.md) | synthesis | Material Science Agents, ACE for Materials, ACE Framework |
| 2026-04-08 | [Claude Code Leak Architecture Insights](derived/claude-code-leak-architecture-insights.md) | article | Agentic Harness, Tiered Memory, Context Engineering |
| 2026-04-08 | [Agentic Service Warmup Plan](derived/agentic-service-warmup-plan.md) | article | Material Science Agents, ACE for Materials, Tiered Memory |
| 2026-04-08 | [Career Development Roadmap](derived/career-development-roadmap.md) | article | Agentic Harness, Material Science Agents, ACE Framework |
| 2026-04-08 | [Lint Report 2026-04-08](derived/lint-report-2026-04-08.md) | lint-report | — |
| 2026-04-08 | [Material Science Agent 入職行動計劃](derived/onboarding-action-plan.md) | article | ACE Framework, ACE for Materials, Material Science Agents |
| 2026-04-08 | [Gemini 諮詢：Patsnap 職涯決策全紀錄](derived/gemini-career-decision-patsnap.md) | session | Material Science Agents, Context Engineering |
| 2026-04-08 | [ChatGPT 諮詢：Patsnap 面試準備與職涯策略](derived/chatgpt-patsnap-interview-strategy.md) | session | Material Science Agents, Context Engineering |
| 2026-04-09 | [OpenAI 目標職位分析與轉職策略](derived/openai-target-role-strategy.md) | session | Material Science Agents, Context Engineering, Agentic Harness |
| 2026-04-09 | [AI Agent 產品案例研究](derived/2026-04-09-agent-product-case-studies.md) | article | Agentic Harness, Agent Product Design, Agent Evaluation |
| 2026-04-09 | [Warmup × KB 缺口分析](derived/2026-04-09-warmup-agent-knowledge-gap-analysis.md) | article | Agent Product Design, Agent Evaluation, Material Science Agents |
| 2026-04-10 | [Hermes Agent: Self-Improving Open-Source AI Agent Framework](derived/2026-04-10-hermes-agent-summary.md) | repo | Hermes Agent Architecture, Three-Tier Memory Systems, ACE Framework, Agentic Self-Improvement |
| 2026-04-15 | [Bouldering Session Weakness Diagnosis](derived/2026-04-15-bouldering-session-diagnosis.md) | session | Climbing Power Endurance, Climbing Lock-Off Strength, Climbing Compression Pulling |
| 2026-04-17 | [RTK (Rust Token Killer)](derived/2026-04-17-rtk-token-killer.md) | repo | RTK Token Killer, CLI Output Compression, Information Theory for LLM Context |
| 2026-04-17 | [Boris Cherny's Claude Code Tips](derived/2026-04-17-bcherny-claude-code-tips.md) | article | Claude Code Token Efficiency Playbook, Agentic Harness |
| 2026-04-17 | [Managed Agents + RLPR: Career Impact](derived/managed-agents-career-impact.md) | synthesis | Claude Managed Agents, RLPR, Material Science Agents |
| 2026-04-18 | [Bouldering Session Debrief 2026-04-17 (Fri Gym)](derived/2026-04-18-bouldering-session-debrief.md) | session | Climbing Lock-Off Strength, Climbing Compression Pulling, Climbing Training System |
| 2026-04-22 | [Bouldering Session Debrief 2026-04-21 (Tue, aborted)](derived/2026-04-22-bouldering-session-debrief.md) | session | Climbing Compression Pulling, Climbing Lock-Off Strength, Climbing Training System |
| 2026-04-23 | [Extraction Pipeline Composite Strategies](derived/2026-04-23-extraction-pipeline-composite-strategies.md) | session | Self-Consistency Implementation, LLM-as-Judge, Verifier Model, Constrained Decoding, Retrieval-Augmented Verification, Self-Refine / Critic Loop, Model Ensembling, Logprob Uncertainty, Active Learning Loop |

---

## Queries

> Logged Q&A sessions and search results.

| Date | Query | Summary |
|------|-------|---------|
| 2026-04-09 | [職涯執行計畫](queries/2026-04-09-career-execution-plan.md) | Patsnap → 300k+ Applied AI 的完整時間線（入職前/初期/中期/跳槽） |
| 2026-04-17 | [RTK + 本 repo 優化路線](queries/2026-04-17-rtk-repo-optimization.md) | RTK 套用評估 + P0/P1/P2 優化清單（基於 Boris Cherny tips） |
| 2026-04-20 | [RTK 與本地 vs 雲端 agent](queries/2026-04-20-rtk-local-vs-cloud-agents.md) | Codex/Devin 為何裝不了 RTK；IDE 位置 ≠ 執行位置；衍生新 concept |

---

## 個人訓練 (Personal Training)

> Personal knowledge bases compiled from curated training resources.

| Topic | Articles | Source |
|-------|----------|--------|
| [Climbing Training System](concepts/climbing-training-system.md) | 1 concept article (parent) | YouTube playlist — 78 videos by yang yu tseng |
| [Climbing Lock-Off Strength](concepts/climbing-lock-off-strength.md) | 1 concept article | EpicTV, Lattice Training, Adam Ondra |
| [Climbing Power Endurance](concepts/climbing-power-endurance.md) | 1 concept article | Lattice Training, Hooper's Beta |
| [Climbing Compression Pulling](concepts/climbing-compression-pulling.md) | 1 concept article | Lattice Training, Hooper's Beta |
| [5 週個人訓練計劃 (V4-V5 → V6-V7 level)](../raw/climbing/climbing-training-plan-summary.md) | training plan | 2026-04-26 重新定義：stable V6-V7 多月工程；5/16 改為 milestone（非驗收）；5/18 入職後進 sustainable cycle |
| [Weeks 2-5 Execution Plan (W3-W5 archived 2026-04-26)](../raw/climbing/weeks-2-to-5-execution-plan.md) | execution plan | **§W3-W5 已 superseded** by Foundation Salvage Block；Week 2 紀錄仍有效 |
| **[Aggressive 21-Day Plan (4/26→5/17, Path C)](../raw/climbing/aggressive-21-day-plan-2026-04-26-to-05-17.md)** | **execution plan (主計劃)** | **目標 5/16-17 雙日 stable V6-V7（V6×4+ / V7 quality attempts ≥ 5）；攀岩 + 飲食 + 睡眠 + 補充品全 sync；7 個 abort gates；機率 55-65% full sync** |
| [Foundation Salvage Block (fallback path)](../raw/climbing/foundation-salvage-block-2026-04-27-to-05-17.md) | fallback plan | aggressive 計劃 abort 時的保守路徑：Phase 0 病期 + Phase 1 V5 重建 + Phase 2 V6×2 milestone（非 stable）|
| [Post-Job Sustainable Plan (5/18 起)](../raw/climbing/post-job-sustainable-plan.md) | long-term plan | 3x/週模板 + 4 週 micro-cycle × 4 cycles → stable V6-V7（C1 適應 → C2 V6 flash 啟動 → C3 V6 多風格 → C4 V6-V7 stable）|
| [Session Diagnosis 2026-04-15](derived/2026-04-15-bouldering-session-diagnosis.md) | session log | Week 1 — 2 × V7 Moonboard attempts |
| [Training Plan 2026-04-17 (Fri)](../raw/climbing/training-plan-2026-04-17-fri.md) | daily plan | Gym pull + weakness-targeted session |
| [Session Debrief 2026-04-17 (Fri Gym)](derived/2026-04-18-bouldering-session-debrief.md) | session log | Plan executed; bicep chain = cross-session rate-limiter; fueling flagged |
| [Weekend Plan 2026-04-18 (Sat Peak + Sun Rest)](../raw/climbing/training-plan-2026-04-18-weekend.md) | weekend plan | Sat V7 project (LAST CALL / LAPUTA) + Sun full rest |
| [Training Plan 2026-04-20 (Mon Active Recovery)](../raw/climbing/training-plan-2026-04-20-mon.md) | daily plan | Deload day — bicep/tricep DOMS 48hr post Laputa; mobility + 血流 |
| [Training Plan 2026-04-21 (Tue Volume + 4×4 PE)](../raw/climbing/training-plan-2026-04-21-tue.md) | daily plan | Week 2 Mon 內容順延一天；PE 啟動日，保守 grade 選路，二頭 chain 持續監測 |
| [Session Debrief 2026-04-21 (Tue, aborted)](derived/2026-04-22-bouldering-session-debrief.md) | session log | V5 單一動作 → 雙側二頭 acute overload；第 3 次 bicep chain 獨立訊號；04-18 dosage 框架修正為 capacity gate |
| [Training Plan 2026-04-22 (Wed Acute Recovery)](../raw/climbing/training-plan-2026-04-22-wed.md) | daily plan | Acute recovery —— 上肢零 loading；晨起 3 項觸診決定 Thu hangboard 分支；goal 修正為 V6 breadth + V7 attempt-ready |
| [Training Plan 2026-04-23 (Thu Hangboard Baseline — Branch A)](../raw/climbing/training-plan-2026-04-23-thu.md) | daily plan | 觸診全過啟動分支 A；Emil protocol 保守版；硬上限 +7.5kg；不攀岩 |
| [Training Plan 2026-04-25 (Sat Breadth Day 1 — V3-V5 多風格 Volume)](../raw/climbing/training-plan-2026-04-25-sat.md) | daily plan | Breadth Day 1；10-15 條 / ≥3 風格；禁 V6+ / compression / Laputa；Fri gym 取消後熱身延長補下肢激活；chain clean window day 5 目標 |
| [Training Plan 2026-04-26 (Sun 急性疾病覆寫 day 1)](../raw/climbing/training-plan-2026-04-26-sun.md) | daily plan | **疾病覆寫**：晨起確認疑似支氣管炎 → 全休；Week 3 Mon 分支決策凍結；chain clean window 凍結（非 reset）|
| [Training Plan 2026-04-27 (Mon 病期 day 2 全休)](../raw/climbing/training-plan-2026-04-27-mon.md) | daily plan | 取代原 W3 Branch A；day 2 病程方向判讀；明日三階決策準備 |
| [Training Plan 2026-04-28 (Tue 三階決策 — Tier A/B/C)](../raw/climbing/training-plan-2026-04-28-tue.md) | daily plan | 取代原 W3 Tue gym；晨起症狀讀 → A 全休 / B 散步 + 伸展 / C 50% 健身（禁上肢、禁攀岩）|

<!-- END AUTO-GENERATED -->

---

## Notes

> Manual notes — not overwritten by automation.

*(Add free-form notes here.)*
