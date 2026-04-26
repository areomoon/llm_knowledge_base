---
name: climbing-schedule
description: Generate a concrete, exercise-level climbing training plan for a specific day, weekend, or week — output goes to `raw/climbing/training-plan-<YYYY-MM-DD>[-<slot>].md` and is indexed in `wiki/index.md`. Trigger on "排訓練表", "排這週訓練", "generate training plan", "plan this weekend", "幫我排 X 月 X 日的訓練", or any request to schedule a climbing session that has not yet been written up.
---

# Climbing Training Schedule Generator

This skill produces **prescriptive, exercise-level** daily plans anchored to the user's 5-week periodisation, adjusted for the most recent session debrief, and formatted for direct execution on the gym floor.

The canonical output format is `raw/climbing/training-plan-2026-04-17-fri.md` and `raw/climbing/training-plan-2026-04-18-weekend.md` — mirror those exactly (structure, table columns, authority citations). **Do not invent a new layout.**

---

## Inputs (ask if missing)

- **Target date(s)**: single day, a weekend, or a full week. Accept either absolute dates or relative ("this weekend", "本週").
- **Week number** within the 5-week cycle (Week 1 = 2026-04-13 start; derivable from date).
- Whether the user wants **single file** (one document covering all days) or **one file per day** — default: single file if 1-2 days, one file per day for full week.

---

## Pre-flight diagnostic (added 2026-04-26 — answer ALL before planning)

Before generating any plan, explicitly answer the following. **Do not proceed if any answer is unknown** — ask the user. This blocks the most common bias: planning with implicit assumptions that turn out wrong.

### 1. Goal type — single-day verification vs. stable steady-state

| Type | Definition | Implication |
|------|-----------|-------------|
| **Single-day milestone** | One performance day demonstrating a peak (e.g. V6×3 different styles in one Sat) | Achievable in 4-6 weeks of focused training for a returning climber; plan as peak/verification cycle |
| **Stable steady-state** | Operational range maintained across multiple sessions (e.g. V6 flash 6+ stocked, V7 quality attempts repeatable, chain tolerates consecutive training) | Multi-month build; single 5-week cycle is foundation only |

**Failure mode if conflated**: original 04-13 plan promised "V6 level by 5/17" implying single-day, user's actual goal was steady-state — gap surfaced at 2026-04-26 conversation. **Always ask which one.**

### 2. External hard deadlines

- Job start / change date?
- Travel / unavailable windows?
- Exam / life event?

If yes → **reverse-engineer cycle from deadline backward**, do not extend. **Failure mode**: original plan didn't ask about 5/18 job start; user's hard deadline was discovered mid-cycle and forced re-plan.

### 3. Climber profile — returning vs. new

- **Returning climber** (peak history at goal grade, currently de-trained): 2-3× faster adaptation than new climber to same grade. Lattice's "V5→V7 typical 3-9 months" applies to **new** climbers.
- **New climber** (never been at goal grade): use literature timeline.

**Failure mode**: 2026-04-26 evening I quoted "16-24 weeks to stable V6-V7" using new-climber timeline for a returning climber → 4× overestimate.

### 4. Current health status

- Any illness in past 7 days? Any active symptoms?
- If illness present → **apply Eichner neck-check rule** (above-neck = light OK; below-neck = full rest until 24hr symptom-free) + ACSM return-to-train 50% volume first week.

### 5. Active capacity-gate rate-limiters

Read latest 2-3 debriefs for any muscle group / pattern with **≥ 2 independent failure signals**. If yes:
- It is a **project-level rate-limiter** (not session-level dosage knob)
- Plan must respect cross-session clean window before re-loading
- See [2026-04-22 debrief §6](../../wiki/derived/2026-04-22-bouldering-session-debrief.md) for clean window operational definition

**Failure mode**: 04-15 LAST CALL compression failure was visible signal #1; 04-17 typewriter was #2; should have flagged bicep chain as project-level rate-limiter at #2, not #3 (04-21 acute event).

### 6. Probability framing — never promise determinism

For any plan that targets a specific outcome (verification day, milestone), state probability honestly:
- "≈ X% IF conditions A, B, C hold"
- List abort gates explicitly
- Provide fallback path

**Failure mode**: original 04-13 plan implied 5/17 V6×3 was deterministic. Real probability with a returning climber + peak history + 0 setbacks ≈ 50-60%. Never call a plan "達標" without contingencies.

### 7. Life-sync dimensions — diet + sleep + lifestyle

For any aggressive plan (probability < 70%), explicitly include diet + sleep + supplements + lifestyle constraints. **+15-20 percentage points on probability** comes from full life sync (Walker *Why We Sleep*; Cohen 2009 sleep+immune; Keith Baar collagen). Plans that only program training under-deliver vs. integrated plans.

> See [aggressive-21-day-plan-2026-04-26-to-05-17.md](../../../raw/climbing/aggressive-21-day-plan-2026-04-26-to-05-17.md) as the canonical integrated example.

---

## Required reads (in this order)

1. **`raw/climbing/climbing-training-plan-summary.md`** — 5-week periodisation, profile (32M/173/72kg, 引體 20 下), Bottlenecks, weekly structure template (Mon Volume / Tue Gym / Wed Rest or Climb / Thu Hangboard / Fri Gym / Sat Peak / Sun Rest).
2. **`raw/climbing/weeks-2-to-5-execution-plan.md`** — week-specific templates with concrete exercises. Find the section matching the target week; copy its structure as the baseline.
3. **Latest session debrief** — glob `wiki/derived/*-bouldering-session-*.md` (descending date) and the matching `raw/climbing/session-*/session-notes.md`. The *most recent* debrief drives carry-forward adjustments (see §Carry-forward rules).
4. **`raw/climbing/exercise-reference.md`** — authoritative exercise instruction book. Use it to verify sets/reps/rest and authority citations.
5. **Concept articles** at `wiki/concepts/climbing-lock-off-strength.md`, `climbing-compression-pulling.md`, `climbing-power-endurance.md`, `climbing-training-system.md` — for authority citations on each prescribed exercise.

---

## Output file

### Location
`raw/climbing/training-plan-<YYYY-MM-DD>[-<slot>].md` where `<slot>` is `fri`, `sat`, `weekend`, `week-N`, etc. Use the **start date** for multi-day files.

### Frontmatter template
```yaml
---
title: "Training Plan — <YYYY-MM-DD> <day> (Week N, <slot>)"
date: <YYYY-MM-DD>
cycle: 5-week plan, Week <N> (<phase>), Day <n>
scheduled_type: <gym type / rock type / rest>
tags: [climbing, training-plan, <day-specific tags>]
---
```

### Body structure (mirror `training-plan-2026-04-17-fri.md`)

Every training day MUST include:

1. **Header block** (bullet list above A):
   - 總時長
   - 類型
   - 特化調整（今日 specific tuning vs. generic template）
   - 本週實際節奏 recap (Mon→Sun one-liner)
   - 恢復脈絡（T+N from last hard finger day / last hard bicep day, explicit）
   - Any gap/flag carried from last debrief

2. **目標（今日 specific）** — numbered list, 3–5 items, concrete not vague
   - ❌ "get stronger"
   - ✅ "左側 lock-off 單側訓練 — 量 ≥ 右側"

3. **A-through-E blocks** — each with a table having these columns:
   | # | 動作 | 組 × 次/秒 | 休息 | 備註 |
   
   Block naming depends on day type:
   
   **Gym day** (Tue / Fri):
   - A. 熱身
   - B. Main block (theme — e.g. lock-off, compression, pull-power)
   - C. Secondary block (complementary group)
   - D. Core
   - E. 拮抗 + 收操
   
   **岩館 day** (Mon Volume / Wed Hard / Sat Peak):
   - A. 熱身（含 dead hang recirculation + V2-V3 flash）
   - B. Flash 區（V4-V5 建立手感，不吃 attempts 配額）
   - C. Main on-wall work — Volume (4×4 PE) / Hard climb (V6 project) / Peak (V7 project with attempt配額 hard cap)
   - D. 補量 / technique run (conditional — drop if fingers死)
   - E. 收操
   
   **Hangboard day** (Thu):
   - A. 熱身（10–15 min，含 bodyweight hang ramp）
   - B. Max hang protocol（Emil Abrahamsson — 20mm, 10s × 5, rest 3-5 min）
   - C. 輕量攀岩 V3-V4 technique
   - D. 收操
   
   **Rest day** (Sun / Wed in some weeks):
   - Table of 擇 1-2 項 active recovery options (散步 / 瑜珈 / 泡澡 / 滾筒 / 輕度下肢)
   - 飲食 + 睡眠 + 明確不做 list
   - Morning check-in 5-item form

4. **Each block MUST have an authority footer**:
   > 依據：[Concept Name](../../wiki/concepts/<slug>.md) — <authority>, <work title>
   
   Valid authorities: Lattice Training, Hooper's Beta, Adam Ondra, Emil Abrahamsson, Keith Baar, EpicTV, Magnus Midtbø, TAMY Climbing, Shauna Coxsey, Ned Feehally. **No un-cited prescriptions.**

5. **刻意避開的內容（今日不做）** — ❌ bullet list with reason per item

6. **監測 KPI（今日記錄）** — checkbox list, 5–8 items, day-specific. Peak days get more (attempt count, highest hand per project, L/R feel). Gym days get load numbers (pinch kg, offset pull-up reps by side).

7. **明日預告** — one-line preview of next day's cycle role

8. **生成來源** — links to the source files consulted

### Project/Peak day extras (Sat, or any project attempt session)

The C block on project days MUST include:
- **Decision point** (typically from A8) that determines which project is primary vs. backup
- **Attempt 配額 hard cap** by week (Week 1: 6, Week 2-3: 6-8, Week 4: 8, Week 5: 6)
- **Attempt flow** with explicit step list: attempt #1 → attempt #2 → active recovery (V3-V4) → section work (does NOT count against cap) → link attempt → conditional continuation
- **4 stop-loss signals**: finger pain/swelling, sharp bicep/elbow flexor tug, 3 consecutive regressions, forearm pump > 7/10
- **Nutrition section** above A (collagen 15g + VitC 50mg 60 min pre; carbs 60-80g + protein 20-30g 2 hr pre stop food; caffeine 3-5 mg/kg 30-45 min pre; post-climb 30g protein + 60-80g carbs within 30 min)
- **🧠 核心概念 explainer block** placed between B and C. Jargon is opaque without it; the user has to be able to read the plan and understand why 配額 / section work / 補量 / D-block conditionality exist. Required subsections:
  1. Two independent budgets table (手指 max-effort 配額 vs 總訓練量 budget —額度, 由誰燒, 恢復週期)
  2. Attempt 配額 definition (一次 attempt = start hold 到掉落; cross-project shared)
  3. Section work 不算配額 rationale (2-3 手, 5-10s output, ≤ 20 min total)
  4. Active recovery (V3-V4) 不算配額
  5. 補量 rationale (為什麼 D block 存在 + 為什麼需要指力 ≥ 50%)
  6. A decision flowchart (C 跑完 → 手指配額用完？→ 總訓練量還剩？→ 做 D / 跳到 E)
  7. One-sentence summary: "最珍貴資源（手指）→ 最高價值事（V7）；剩的能量 → 鞏固性工作（V5-V6 量）"
  Reference from C2 (備選共用配額) and D (此 block 在做什麼) blocks using `§核心概念 N️⃣`.

---

## Carry-forward rules (from latest debrief → today's plan)

Read the most recent debrief and apply:

| Signal in debrief | Adjustment to generated plan |
|---|---|
| Muscle group flagged as cross-session rate-limiter (e.g. bicep/elbow-flexor) | Reorder: do not stack that group 3rd-4th in a session; move dependent exercises earlier or to a different day |
| Fasted session → tail block dropped | Add nutrition table **above A**, flag as non-optional |
| Exercise selection validated | Keep structure; adjust dosage only |
| Exercise selection invalidated | Swap to alternative from `exercise-reference.md` matching the same concept tag |
| T+1 from hard unilateral day | Peak day: flag "首 attempts 會感覺重, 預期內"; add A8 check to gate primary project choice |
| Missed hangboard baseline | Inject as Week-2 Thu補測 line in 明日預告 or next-week preamble |
| Sleep or weight KPI off-target | Add explicit line in 頭部 header (not buried in KPI section) |
| **Acute illness reported (any below-neck symptom)** | Apply illness override: kill ALL training (incl. active recovery walk/foam roll); replace with bed rest + symptom monitor + return-to-train Tier A/B/C decision matrix; freeze any in-flight readout windows (chain clean window etc.) — do not reset, just pause; reference Eichner neck-check rule as authority |
| **Acute illness — return-to-train** | First week back ≤ 50% volume (ACSM); reintroduce sport-specific (climbing/hangboard) only after 24hr fully symptom-free; bicep chain etc. clean window counts must rebuild from scratch (病期 deconditioning) |
| **External hard deadline appears** (job, travel, exam) | Reverse-engineer cycle backward from deadline; do NOT extend; if illness + hard deadline collide, present probability with conditions + abort gates, never promise determinism |
| **Capacity-gate signal #2 in last 2 weeks** | Upgrade muscle group / pattern from session-level dosage knob to **project-level rate-limiter**; require ≥ 2 consecutive clean sessions before re-loading the provoking grade. **Do not wait for signal #3.** |
| **User's stated goal is "stable / 穩定 / 持續"** (steady-state, not single-day) | Plan must explicitly distinguish single-day milestone vs steady-state; if cycle window < 8 weeks, single-day milestone is realistic, steady-state needs multi-cycle horizon — say so |

If there is **no debrief since the last plan**, note this explicitly in 頭部 header ("無新 debrief，沿用 standard template") and do not invent adjustments.

---

## Indexing

After writing the plan file, update `wiki/index.md` — add a row to the **個人訓練 (Personal Training)** table:

```markdown
| [<Plan title>](../raw/climbing/<filename>.md) | <type label> | <one-line hook> |
```

Place the new row **below** the existing daily-plan rows, maintain chronological order. Do not touch the Stats block (plans are raw files, not derived notes — they do not change wiki counts).

---

## Sanity checklist before finishing

- [ ] Every block has a table with columns `# / 動作 / 組 × 次/秒 / 休息 / 備註`
- [ ] Every block has an authority footer citing a named source
- [ ] 岩館 days have an on-wall C block with concrete V-grade targets (not "project V7" alone — name the problems: `LAST CALL` / `LAPUTA` / etc.)
- [ ] Peak days have: A8 decision point → attempt cap → attempt flow → 4 stop-loss signals → nutrition table
- [ ] 刻意避開 list has ≥ 3 items with per-item reason
- [ ] KPI checkbox list is day-specific (not generic)
- [ ] 生成來源 links point to actual files that exist on disk
- [ ] File indexed in `wiki/index.md` Personal Training table
- [ ] No authority-less prescriptions ("it's well known that…") — every exercise traceable to Lattice / Hooper / Ondra / Abrahamsson / Baar / EpicTV / Midtbø / TAMY / Coxsey / Feehally

---

## Watch-outs

- **Rest days are rest** — do not invent 岩館 content for Sun. The 5-week plan is explicit: Sun = full recovery. But **do** give rest days the same table structure (options table + checkboxes), not prose.
- **Section work ≠ attempts** — when writing Peak day flows, make this distinction explicit; it changes the effective cap.
- **T+N finger accounting** — always compute days since the last heavy-finger session (Moonboard / hangboard max / project day). Peak day expects T+2 minimum; T+1 is a red flag that should raise finger-load avoidance in the plan.
- **Don't stack tendon load** — back-to-back hangboard + hard climb is a Week-3+ move, not Week-1. If the user asks for it in Week 1, push back and propose splitting.
- **Week boundaries**: Week N = 7 consecutive days starting Mon. The 5-week cycle anchor is Mon 2026-04-13 (Week 1 Day 1). Compute week number from that.

---

## Calibration gotchas (observed 2026-04-26 — read first)

Real planning errors made on this user's cycle. Each row = a bias to actively counteract.

### G1. Single-day verification ≠ steady-state stability

- **Bias**: Use "V6 level" or "V7 attempt-ready" without operational definition; user assumes one thing, plan delivers another.
- **Counter**: §Pre-flight diagnostic Q1 forces explicit goal type. If user says "stable / 穩定", plan must include cross-session repeatability KPI (e.g. Sun ≥ Sat 70% on dual-day verification), not single-day peak only.

### G2. New-climber vs. returning-climber timeline conflation

- **Bias**: Quote Lattice's "V5→V7 typical 3-9 months" for a returning climber → 2-4× overestimate.
- **Counter**: §Pre-flight Q3 — if returning climber (peak history at goal grade), divide literature timeline by 2-3. Use the user's own prior cycle data when available, not generic literature.

### G3. Rate-limiter detected too late (signal #3 instead of #2)

- **Bias**: Treat each setback as isolated; only formalise "project-level rate-limiter" after 3 independent signals.
- **Counter**: New Carry-forward row "Capacity-gate signal #2 in last 2 weeks" — escalate at signal #2, not #3. The cost of false positive (1 week of conservative loading) << cost of false negative (acute event aborts session).

### G4. No setback buffer in cycle design

- **Bias**: 5-week plan assumes 0 illness, 0 missed sessions, 0 work disruption.
- **Counter**: Bake in 10-20% setback buffer at cycle design time. If user requests aggressive plan with no buffer, state explicitly: "this plan succeeds at ~X% with 0 setbacks; each lost week drops it by ~10-15%".

### G5. Plans framed as deterministic ("達標") rather than probabilistic

- **Bias**: "5/17 V6×3" framed as goal to be hit, not probability to be optimised.
- **Counter**: §Pre-flight Q6 — every aggressive plan states honest %, conditions, abort gates, and fallback path.

### G6. External hard deadlines discovered mid-cycle

- **Bias**: Plan generated 04-13 didn't ask about post-cycle commitments; 5/18 job start surfaced 04-26.
- **Counter**: §Pre-flight Q2 — always ask. If user adds a hard deadline mid-cycle, immediately re-plan rather than continuing the old structure.

### G7. Training-only programming under-delivers vs. integrated programming

- **Bias**: Plans that program only on-wall + gym, leaving diet/sleep/supplements/lifestyle as "guidelines".
- **Counter**: For probability < 70% plans, integrate diet + sleep + lifestyle as first-class blocks (see [aggressive-21-day-plan-2026-04-26-to-05-17.md](../../../raw/climbing/aggressive-21-day-plan-2026-04-26-to-05-17.md) as canonical integrated example). Quantify the +15-20 pp probability uplift from full sync.

### G8. Pendulum swings between aggressive and conservative

- **Bias**: After a setback, overcorrect to ultra-conservative; after pushback, overcorrect to ultra-aggressive. Both degrade trust.
- **Counter**: Anchor estimates in user's empirical adaptation rate (prior cycle data) when available. When unavailable, give a range with named conditions and **resist the urge to revise mid-conversation without new data**. If a number changes, name what new information drove it.
