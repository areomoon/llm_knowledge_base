---
title: "专访前FAIR研究总监田渊栋：Meta裁员之后，对AI的一些遗憾与思考"
source: https://www.youtube.com/watch?v=EsaUQNx59vA
channel: 硅谷101 (Silicon Valley 101)
guest: 田渊栋 (Yuandong Tian), 前 Meta FAIR 研究总监
date: 2025-11-10
duration: "39:09"
views: 332110
tags: [FAIR, Meta, scaling-law, RL, LLM-limitations, AI-talent, open-source, AGI, career]
---

# 专访田渊栋：Meta 裁员后的 AI 反思

## 背景
2025年10月底，Meta AI 部門大裁員約 600 人。田渊栋是 Meta FAIR 工作十年多的研究總監，是這次裁員的核心人物之一。硅谷101 對他進行了深度專訪。

## 核心觀點按時間線

### 1. 被裁並不意外（02:33-07:51）
- 被裁是「一次被加速的個人選擇」
- 在 Meta 十年，對離開已有心理準備

### 2. AI 正在自動化 AI 本身（07:51-10:02）
- **行業大趨勢**：AI 自動化程度提高，未來「執行層」的人會越來越少
- 這跟 ACE Framework 的「agent 自我改進」理念高度呼應
- 對 areomoon 的啟示：你的 Algorithm Expert 角色正好在「設計層」而非「執行層」，是相對安全的位置

### 3. 開源會繼續，但「用途」才是核心（10:02-13:31）
- 開源模型本身不是問題，問題是如何把模型變成有用的產品
- 模型的「用途」比模型本身更有價值
- 對 areomoon：Patsnap 把 LLM 應用在 patent analytics 就是典型的「用途」驅動

### 4. LLM 的最大問題：效率低下（13:31-16:17）
- **核心論點**：LLM 需要海量數據，梯度下降（gradient descent）並不是好方案
- 人類學習效率比 LLM 高千倍
- LLM 的 data-hungry 特性是根本性限制

### 5. 強化學習的潛力：主動學習（16:17-19:04）
- RL 讓 AI「主動學習」，可以產生更高質量的數據
- 不需要像 supervised learning 那樣被動接收數據
- 跟 RLPR 論文的理念一致（用 LLM 自身的機率信號當 reward）
- 跟 ACE 的 Generator-Reflector-Curator 循環也呼應

### 6. Scaling Law 是悲觀的未來（19:04-24:57）
- **爆炸性觀點**：Scaling Law 意味著你必須不斷投入更多計算資源才能獲得 marginal improvement
- 這不是一個 sustainable 的路徑
- AGI 仍需幾十年，不是幾年
- 需要根本性的新 paradigm，不只是更大的模型

### 7. 人類洞察力難以取代（24:57-26:38）
- 研究方向的選擇、問題的定義 — 這些是人類的核心價值
- AI 可以加速執行，但「what to work on」的判斷力是不可替代的
- 他的下一步：結合前沿研究與自動化應用

### 8. 連續思維鏈研究（26:38-28:34）
- 在被裁之前，他在研究 continuous chain-of-thought（連續思維鏈）
- 這跟 discrete token-based CoT 不同，是在 latent space 做推理
- 救火 Llama 4 的工作經歷

### 9. FAIR 十年回顧（28:34-31:14）
- **最大遺憾**：工程做得太少。純研究和實際產品之間有巨大 gap
- **最大收穫**：培養了「研究品味」（research taste）— 知道什麼問題值得花時間
- 這跟你的入職策略呼應：不要只做 engineering，也要培養 research intuition

### 10. AI 人才戰的反直覺建議（31:14-34:28）
- **核心建議**：不要追逐「稀缺性」
- 市場信號是滯後的 — 當你看到某個領域「稀缺」時，大量人已經湧入了
- 應該追隨興趣而非市場信號
- 「做你真正想做的事」比「做市場認為值錢的事」更有長期回報
- 跟「35 歲碼農」那篇文章的「接受自己是普通人」觀點互補

### 11. 理想主義科學家的下一步（34:28-39:09）
- 應用與研究的交匯點是最有價值的位置
- 不是純研究，也不是純工程
- 是「用研究的深度去解決實際問題」

## 對 areomoon 的關鍵啟示

1. **你的位置是對的**：Algorithm Expert 在「設計層」，不在「執行層」。AI 自動化執行層但需要人設計
2. **Research taste 很重要**：入職後不只要寫 code，要培養「什麼值得做」的判斷力
3. **RL > 純 supervised**：你的 ACE + RLPR 學習方向是對的，田渊栋也認為 RL 是突破 LLM 瓶頸的關鍵
4. **Scaling Law 的局限**：不要迷信「更大模型 = 更好」，context engineering / harness engineering 才是實際的 leverage
5. **追隨興趣**：Material Science × AI Agent 是你真正感興趣的交集，這比追逐市場熱點更有長期價值
6. **工程不能少**：田渊栋最大遺憾是工程做太少。你的 side projects（ai_daily_digest, sg_rental_finder, knowledge_base）正好補了這個缺口

## 參考
- 影片：https://www.youtube.com/watch?v=EsaUQNx59vA
- 頻道：硅谷101 https://www.youtube.com/@sv101
- 田渊栋 X：@tydsh
- 相關影片：失衡的乌托邦：Meta的开源AI路线是如何遭遇滑铁卢的 https://www.youtube.com/watch?v=0mrko3cYqBs
