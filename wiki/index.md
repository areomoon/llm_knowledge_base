# LLM Knowledge Base — Index

> This index is maintained by Claude Code Agent. See [CLAUDE.md](../CLAUDE.md) for compile instructions.
> Manual notes go in the [Notes](#notes) section — they will not be overwritten.

---

<!-- AUTO-GENERATED -->

## Stats

| Metric | Count |
|--------|-------|
| Concept articles | 28 |
| Derived notes | 16 |
| Query records | 2 |
| Last compiled | 2026-04-17 |

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
| [CLI Output Compression](concepts/cli-output-compression.md) | Per-command filter/group/truncate/dedup of shell output before it enters LLM context; regex vs. structural-parsing approaches | `context-compression`, `agentic-harness`, `tooling`, `parsing` |
| [Information Theory for LLM Context](concepts/information-theory-for-llm-context.md) | Shannon entropy framing of why LLM-facing text is 80–95% redundant and where the practical compression ceiling sits | `information-theory`, `shannon`, `context-compression`, `entropy`, `economics` |
| [Claude Code Token Efficiency Playbook](concepts/claude-code-token-efficiency-playbook.md) | Boris Cherny's tips synthesised: effort levels, auto-compact window, worktrees, hooks, /simplify /batch, CLAUDE.md discipline | `claude-code`, `token-efficiency`, `bcherny`, `worktree`, `hooks`, `skills` |
| [Subagent Dispatch Economics](concepts/subagent-dispatch-economics.md) | Cost model for Claude Code's Agent/Task dispatch — when to inline, when to parallelise, when to bound thoroughness | `claude-code`, `subagent`, `dispatch`, `token-efficiency`, `bcherny` |
| [Mobile Dispatch Workflow](concepts/mobile-dispatch-workflow.md) | iPhone / remote Claude Code operating regime — no worktrees, no local hooks; Mac-launched long tasks + mobile check-in via /loop, /schedule, /btw | `claude-code`, `mobile`, `iphone`, `remote-development`, `dispatch`, `bcherny` |

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

---

## Queries

> Logged Q&A sessions and search results.

| Date | Query | Summary |
|------|-------|---------|
| 2026-04-09 | [職涯執行計畫](queries/2026-04-09-career-execution-plan.md) | Patsnap → 300k+ Applied AI 的完整時間線（入職前/初期/中期/跳槽） |
| 2026-04-17 | [RTK + 本 repo 優化路線](queries/2026-04-17-rtk-repo-optimization.md) | RTK 套用評估 + P0/P1/P2 優化清單（基於 Boris Cherny tips） |

---

## 個人訓練 (Personal Training)

> Personal knowledge bases compiled from curated training resources.

| Topic | Articles | Source |
|-------|----------|--------|
| [Climbing Training System](concepts/climbing-training-system.md) | 1 concept article (parent) | YouTube playlist — 78 videos by yang yu tseng |
| [Climbing Lock-Off Strength](concepts/climbing-lock-off-strength.md) | 1 concept article | EpicTV, Lattice Training, Adam Ondra |
| [Climbing Power Endurance](concepts/climbing-power-endurance.md) | 1 concept article | Lattice Training, Hooper's Beta |
| [Climbing Compression Pulling](concepts/climbing-compression-pulling.md) | 1 concept article | Lattice Training, Hooper's Beta |
| [5 週個人訓練計劃 (V4-V5 → V6-V7)](../raw/climbing/climbing-training-plan-summary.md) | training plan | Generated 2026-04-13, full docx at raw/climbing/ |
| [Session Diagnosis 2026-04-15](derived/2026-04-15-bouldering-session-diagnosis.md) | session log | Week 1 — 2 × V7 Moonboard attempts |
| [Training Plan 2026-04-17 (Fri)](../raw/climbing/training-plan-2026-04-17-fri.md) | daily plan | Gym pull + weakness-targeted session |

<!-- END AUTO-GENERATED -->

---

## Notes

> Manual notes — not overwritten by automation.

*(Add free-form notes here.)*
