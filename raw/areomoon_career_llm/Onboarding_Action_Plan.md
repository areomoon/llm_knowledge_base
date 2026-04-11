---
title: "Material Science Agent 入職行動計劃"
date: 2026-04-08
tags: [career, onboarding, material-science, agent, ACE]
---

# Material Science Agent 入職行動計劃

基於 ACE (Agentic Context Engineering) 框架和現有材料科學 Agent 研究，為即將到來的 Material Science Agent 算法工程師角色制定的行動計劃。

## 短期（入職前，2026年4月-5月）

**重點：理解 MARS 和 LLMatDesign 的架構，特別是 multi-modal + domain tool 整合**

### 必讀論文
- MARS 系統論文：Knowledge-driven autonomous materials research via collaborative multi-agent and robotic system
  - 重點：19 個 LLM agents 如何分工（Orchestrator, Scientist, Engineer, Executor, Analyst）
  - 重點：16 個 domain-specific tools 的整合模式
  - 新聞報導：https://phys.org/news/2026-01-multi-agent-ai-robots-automate.html

- LLMatDesign 論文：https://arxiv.org/abs/2406.13163
  - GitHub 實作：https://github.com/Fung-Lab/LLMatDesign
  - 重點：LLM 如何進行 iterative propose/evaluate/refine
  - 重點：self-reflection 機制如何從過去的決策中學習

- MatAgent：https://github.com/adibgpt/MatAgent
  - physics-aware multi-agent LLM framework

### 學習資源
- Towards Agentic Intelligence for Materials Science (arxiv 2602.00169)
- Agentic material science: https://www.oaepublish.com/articles/jmi.2025.87
- MADE Benchmark for closed-loop materials discovery: https://arxiv.org/abs/2601.20996

## 入職初期（第1-2個月）

**重點：先做 Generator extraction prompt + Reflector self-consistency，比 fine-tuning 更快見效**

### Generator-Reflector Pattern 學習資源
- Andrew Ng - Agentic Design Patterns Part 2 Reflection: https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/
- LangChain Reflection Agents: https://blog.langchain.com/reflection-agents/
- Reflexion 技術指南: https://www.promptingguide.ai/techniques/reflexion
- ACE Playbook 開源實作 (Generator-Reflector-Curator): https://github.com/jmanhype/ace-playbook
- Reflection Agent Pattern 文檔: https://agent-patterns.readthedocs.io/en/stable/patterns/reflection.html
- LangGraph 自我改進 Agent: https://medium.com/@shuv.sdr/langgraph-build-self-improving-agents-8ffefb52d146

### 實戰步驟
1. 設計 extraction prompt template（Generator 角色）
2. 實作 self-consistency check（Reflector 角色）
3. 建立 extraction case 收集機制（為後續 fine-tuning 累積資料）

## 中期（第3-4個月）

**重點：用累積的 extraction case 建 SFT 訓練集做 QLoRA — 與 Warmup Plan Week 5 對齊**

### QLoRA Fine-tuning 學習資源
- QLoRA 原始論文: https://arxiv.org/abs/2305.14314
- QLoRA GitHub: https://github.com/artidoro/qlora
- 2025 實用指南: https://reintech.io/blog/how-to-fine-tune-llms-with-lora-and-qlora-practical-guide
- 2026 完整教程: https://oneuptime.com/blog/post/2026-01-30-qlora-fine-tuning/view
- 深度指南 (LoRA + QLoRA): https://www.mercity.ai/blog-post/guide-to-fine-tune-llms-with-lora-and-qlora/
- LLM Fine-tuning 完整指南 2025: https://tensorblue.com/blog/llm-fine-tuning-complete-guide-tutorial-2025
- Consumer GPU 實戰: https://letsdatascience.com/blog/fine-tuning-llms-with-lora-and-qlora-complete-guide

### 實戰步驟
1. 從入職初期累積的 extraction cases 中整理 SFT 訓練集
2. 選擇基礎模型（推薦先用 Llama 或 Qwen 系列）
3. QLoRA 設定建議：r=16, DoRA, target_modules="all-linear", lr=2e-4, cosine warmup
4. 評估：比較 fine-tuned model vs base model + prompt engineering 的 extraction 品質

## 參考架構連結
- [ACE Framework](../../wiki/concepts/ace-framework.md)
- [ACE for Materials](../../wiki/concepts/ace-for-materials.md)
- [Material Science Agents](../../wiki/concepts/material-science-agents.md)
- [Agentic Self-Improvement](../../wiki/concepts/agentic-self-improvement.md)

---

## 追加：Managed Agents 和 RLPR (2026-04-10 更新)

兩個 2026 年 4 月的新發展，大幅改變入職策略。

### 背景

**Claude Managed Agents** (Anthropic, 2026-04-01 beta)：
- Anthropic 把 ACE Framework 的理論架構變成了 managed cloud service
- Memory Store = managed evolving playbook：agent 在 task 開始前自動讀，結束後自動寫
- 可以替代自己搭 LangChain/LangGraph + ACE Curator 的計劃
- 進入 beta 申請：https://claude.com/form/claude-managed-agents

**RLPR** (OpenBMB, arXiv 2506.18254, 2025-06-23)：
- Reference Probability Reward：用 LLM 對 reference answer 的 token probability 當 reward
- 不需要 domain verifier → 完全適合材料科學 extraction（無法用 unit test 驗證）
- Materials Project / Springer Materials 的結構化資料可以直接當 reference answer → 不需要專家標注就能開始
- 超越需要 verifier 的 General-Reasoner (+1.6 avg)、超越 VeriFree (+7.6 TheoremQA)

### 修訂後的行動計劃

#### 入職前（2026年4月-5月）— 不變
繼續原計劃：讀 MARS, LLMatDesign, MatAgent 論文。
新增：申請 Managed Agents beta + 讀 RLPR 論文。

#### 入職初期（第1-2個月）— 重大更新

**舊計劃**：自己建 Generator extraction prompt + Reflector self-consistency（LangChain/LangGraph）

**新計劃**：
1. 用 **Managed Agents** 搭原型 extraction agent（claude-sonnet-4-6 + bash + web tools）
2. 定義初始 Memory Store 架構：`extraction-heuristics.md`、`per-material-class/oxides.md` 等
3. 跑 20–30 篇論文的 extraction；讓 agent 把規則累積進 Memory Store
4. 比較：有 Memory Store vs 沒有 Memory Store 的 extraction F1

**關鍵提案**：在第一週的架構討論中提出「用 Managed Agents 替代 LangChain/LangGraph」。

#### 中期（第3-4個月）— 更新

**新優先序**（依 ROI 排序）：
1. **Memory Store 調優**（優先）：優化 Memory Store 結構（粒度、deduplication 頻率）
2. **RLPR 基線**（其次）：用 Materials Project 結構化資料當 reference answer；在 Qwen-7B 跑 GRPO + RLPR
   - 設定：r=16, DoRA, cosine warmup, probability reward
3. **SFT 混合**（最後，若 RLPR 到瓶頸）：加入專家標注的 SFT 訓練集

**核心主張**：「RLPR 讓我們不需要專家標注就能開始 RL 訓練。用現有資料庫就能做 reward。」

### 實戰步驟（追加）

入職前：
- [ ] 申請 Claude Managed Agents beta access
- [ ] 讀 RLPR 論文 (arXiv 2506.18254)，重點：prob-to-reward transformation

入職第1-2週：
- [ ] 評估：Patsnap 現有系統用什麼 agent 框架？
- [ ] 在第一次架構討論提出 Managed Agents 方案
- [ ] 定義 Memory Store schema for materials extraction

入職第2個月：
- [ ] 量化 Memory Store 收益：有/沒有 memory 的 extraction 品質對比（50 篇論文）
- [ ] 呈現結果：「Memory Store 不需要標注，提升 X% extraction 品質」

入職第3個月：
- [ ] 建立 RLPR 訓練環境（OpenBMB/RLPR GitHub）
- [ ] 收集 500–1000 個 (paper section, reference answer) pair from Materials Project
- [ ] 跑 RLPR baseline on Qwen-7B

### 技術差異化陳述（面試或架構審查用）

> 「我計劃用 Claude Managed Agents 作為 extraction service 的基礎設施，Memory Store 實作按材料類別分層的 evolving extraction playbook。這讓我們不需要自己寫 ACE Curator 的程式碼就能做到跨 session 的自我改進。在 post-training 方面，RLPR 讓我們可以用現有結構化資料庫的條目當 reward signal 做 RL fine-tuning — 前兩個月不需要專家標注。這個做法降低了基礎設施複雜度，同時加速了改進循環。」

### 參考連結（新增）
- [Claude Managed Agents](../../wiki/concepts/claude-managed-agents.md)
- [RLPR (Reference Probability Reward)](../../wiki/concepts/rlpr-reference-probability-reward.md)
- [Memory Stores vs RAG](../../wiki/concepts/memory-stores-vs-rag.md)
- [Managed Agents Career Impact (Derived Note)](../../wiki/derived/managed-agents-career-impact.md)

---

## 追加：35 歲危機洞察與健康基礎設施 (2026-04-11 更新)

基於「那些 35 歲以上的碼農們，都幹啥去了」（跑哥）的結構性分析，補充職涯韌性框架中缺失的兩個維度：抗螺絲釘化策略與健康基礎設施。

### 背景：為何要警覺於螺絲釘化

中國互聯網大廠（及程度較輕的 SG/US 大公司）存在一種系統性的**螺絲釘化**機制：故意將每個工程師的職責範圍縮到最小，確保沒有人不可替代，從而保持替換彈性。

**對你的直接影響：**
- Patsnap 雖不是中國互聯網大廠，但螺絲釘化在任何規模化科技公司都程度不同地存在
- 如果你的技術深度只在現有職責範圍內，離職時可遷移的技能會比預期的少得多
- **每個 Patsnap 的項目交付物，都應該同時有一個屬於你自己的知識產出**（論文、blog、開源組件）

**抗螺絲釘化的核心行動：**
- [ ] 每個月至少寫一篇 LinkedIn 技術文章（強迫自己把零散工作整合成可遷移的知識）
- [ ] 在 GitHub 維護一個 materials AI 相關的公開 project（哪怕只是 demo 或工具）
- [ ] 每季度做一次「技術廣度評估」：我現在懂多少 end-to-end？我能獨立設計完整系統嗎？

### 健康日常最低標準

**「身體垮了才是真完了」** — 跑哥把健康與螺絲釘化並列為兩大隱形殺手。

健康不是生活方式選擇，是職涯長度的先決條件：

| 指標 | 最低標準 | 備註 |
|------|---------|------|
| 每日步數 | ≥10,000 步 | 遠端工作尤其重要；久坐是慢性殺手 |
| 有氧運動 | 每週 ≥3 次 | 跑步、游泳、騎車均可 |
| 年度健檢 | 每年一次 | 含血壓、血糖、肝腎功能、心血管面板 |
| 通勤時間 | ≤1.5 小時/天 硬性上限 | 見下節 |
| 工時強度 | 不接受長期 996 | 入職談判時明確，不是個人偏好是底線 |

**具體行動：**
- [ ] 手機設定每日步數提醒（目標 10,000 步）
- [ ] 找好 SG 附近的運動場所（入職前先搞定）
- [ ] 在 SG 安頓後第一個月完成全身健檢

### 通勤對家庭健康的複利影響

文章核心警告：通勤在**單身時可承受**，但在**成家後變成計時炸彈**：

- 有了老婆孩子 → 家庭住址需要兼顧多方通勤 → 自己離公司變遠
- 996 + 2-3 小時通勤 = 物理上不可能維持
- 慢性後果：高血壓、高血糖、膽息肉、脂肪肝（這些都是 35-40 歲的典型病史）

**住房選擇原則（現在就要內化）：**
> **地點 > 大小**。買/租房時通勤時間是 tier-1 決策因素，不是 tier-2 的「有更好就好」。
>
> SG 具體：東西兩端通勤可能 1.5-2 小時；選房應優先考慮 Patsnap 辦公室距離，而非房子大小或環境。

- [ ] 選 SG 住房時：Google Maps 測試上班通勤時間，目標 ≤45 分鐘單程

### 弱聯繫網的「在」而非「用」哲學

跑哥的核心觀點：**關係網不是用來「用」的，是用來「在」的**。

這對你的 LinkedIn 策略有直接影響：
- 不是在「需要找工作時」才去聯絡人
- 是**持續讓自己出現在相關人的視野中**，當他們需要人時能想起你
- 每篇技術文章都是在做一次 passive presence update，成本極低，但對整個弱聯繫網有廣播效果

**差異化理解：**
LinkedIn side project 不只是「個人品牌建設」，更是跨公司的弱聯繫網維護基礎設施。這讓你在 30 歲就開始構建「未來的 hiring manager 認識你」的結構性優勢。

### 接受自己是普通人的心態建設

文章最難但最重要的一點：

> 「很多人因為前半生在應試教育裡脫穎而出，不太接受自己是普通人的設定，包袱太重，又容易羡慕那些以前不如你的人爬你頭上去了，就很容易激進冒險把前半生積蓄賠光。」

**對你的應用：**
- 財富計劃的保守底座（W2 + index funds + 房產）是**正確的風險校準**，不是保守主義
- 高風險賭注（創業、高槓杆投資）是**附加項**，絕不是替代項
- 晉升靠部分運氣這件事 → 這正是為什麼不能 all-in W2，而要四軌並行

**核心心態：** 作為一個「相對幸運的普通人」，能靠複利把早年積累轉化為財務自由，已經是非常好的結果。比較基準不是「你可能成為的最頂尖的人」，而是「你現在有什麼選項」。

### 參考連結（新增）
- [China Tech 35-Age Crisis](../../wiki/concepts/china-tech-35-age-crisis.md)
- [Cross-Age Career Resilience](../../wiki/concepts/cross-age-career-resilience.md)
- [35-Age Crisis Summary (Derived Note)](../../wiki/derived/2026-04-11-35-age-crisis-summary.md)
