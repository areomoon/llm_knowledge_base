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
