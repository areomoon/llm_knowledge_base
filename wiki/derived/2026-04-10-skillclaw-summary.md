---
title: "SkillClaw: Collective Skill Evolution with Agentic Evolver"
type: paper
source_url: https://arxiv.org/abs/2604.08377
raw_path: raw/articles/skillclaw-collective-skill-evolution.md
created: 2026-04-10
---

# SkillClaw: Collective Skill Evolution with Agentic Evolver

> **TL;DR**: Agent skills deployed across a multi-user platform can improve autonomously and collectively — an Agentic Evolver aggregates execution trajectories from all users, extracts patterns, and updates the shared skill library without any user effort.

## Key Points

- **Static skills are the core problem**: LLM agent ecosystems like OpenClaw deploy reusable skills (tool-use templates, workflow patterns), but these stagnate post-deployment — each user independently rediscovers the same failure modes.
- **Agentic Evolver solves this**: a dedicated agent continuously reads trajectory logs from all users, identifies recurring successes and failures, and writes mutations back to the shared skill library (refine existing skills + extend with new ones).
- **Zero user overhead**: users never file bug reports; improvement emerges from normal usage.
- **System-wide propagation**: one user's discovery benefits all future users immediately.
- **WildClawBench validated**: evaluated in real OpenClaw environments (bash, browser, email, calendar) with undocumented errors — demonstrates significant improvement for Qwen3-Max on realistic agent tasks.
- **Complementary to ACE**: ACE evolves a per-user playbook; SkillClaw evolves a shared skill library. The two can coexist in the same system.

## Concepts Referenced

- [Collective Skill Evolution](../concepts/collective-skill-evolution.md)
- [Agentic Evolver Pattern](../concepts/agentic-evolver-pattern.md)
- [ACE Framework](../concepts/ace-framework.md)
- [Evolving Playbooks](../concepts/evolving-playbooks.md)
- [Agentic Self-Improvement](../concepts/agentic-self-improvement.md)

## Notes

**Design implications for multi-agent systems:**

The SkillClaw paper formalizes something that was implicit in community-managed skill registries (like the 5400+ skills in OpenClaw's ecosystem): collective knowledge is more robust than individual knowledge. What SkillClaw adds is the *automation* of the curation process — the Evolver replaces the human community maintainer for the subset of improvements that can be derived from trajectory analysis.

**Risk surface unique to collective evolution:**
- Quality pollution at scale (one bad trajectory → bad skill for everyone)
- Privacy leakage across user boundaries
- Skill drift from accumulated micro-mutations (versioning is non-negotiable)

**Relation to this KB's own design:**
This knowledge base uses a similar principle at the *knowledge* level: raw trajectories (conversations, papers) are compiled into concepts by an LLM agent (Claude Code). SkillClaw does the same at the *capability* level: raw trajectories (executions) are compiled into skills by an Evolver agent. The compile step is the common pattern.

## Sources

- [SkillClaw paper (arXiv 2604.08377)](https://arxiv.org/abs/2604.08377)
- [OpenClaw Skills Repository](https://github.com/openclaw/skills)
- [WildClawBench](https://github.com/InternLM/WildClawBench)
- [MetaClaw](https://github.com/aiming-lab/MetaClaw)
