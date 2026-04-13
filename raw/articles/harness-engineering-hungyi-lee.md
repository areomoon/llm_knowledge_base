---
title: "Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導"
source: https://www.youtube.com/watch?v=R6fZR_9kmIw
author: Hung-yi Lee (李宏毅, NTU Professor, 411K subscribers)
date: 2026-04-13
duration: "1:32:21"
views: 3036 (first day)
tags: [harness-engineering, LLM, prompt-engineering, context-engineering, fine-tuning, NTU, hung-yi-lee]
---

# Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導

## 概覽
李宏毅教授（台大）2026年4月13日發布的演講，探討 Harness Engineering — 如何正確「駕馭」語言模型。核心論點：LLM 的能力往往不是問題，問題在於人類如何引導它們。

## 影片資訊
- **頻道**：Hung-yi Lee（411K 訂閱者）
- **時長**：1:32:21
- **發布**：2026-04-13
- **觀看**：3,036（發布後 5 小時）

## 相關系列講座
1. 【生成式AI 2025】第7講：大型語言模型的學習歷程 — https://youtu.be/YJoegm7kiUM
2. 【生成式AI 2025】第8講：通用模型的終身學習 (Fine-tuning, Model Editing, Model Merging, Test-Time Training) — https://youtu.be/EnWz5XuOnIQ
3. 【生成式AI 2025】第三講：AI 的腦科學 — 語言模型內部運作機制剖析 — https://youtu.be/Xnil63UDW2o
4. 【生成式AI 2025】第3講：解剖大型語言模型 — https://youtu.be/8iFvM7WUUs8

## 核心主題：Harness Engineering

Harness Engineering 是近期 AI 領域的熱門概念，強調：
- LLM 本身的能力已經很強，但使用者/開發者如何「駕馭」它才是決定效果的關鍵
- 不是 prompt engineering 的簡單升級，而是更系統性的方法論
- 包含：如何設計 context、如何構建 agent workflow、如何讓 LLM 在特定任務上最大化輸出

## 與知識庫現有概念的關聯

### 跟 ACE Framework 的關係
ACE (Agentic Context Engineering) 的核心就是 Harness Engineering 的子集：
- 如何透過 evolving playbook 讓 LLM 越來越會做特定任務
- Generator-Reflector-Curator 三角色本質上就是「harness」LLM 的系統方法

### 跟 Context Engineering 的關係
Harness Engineering 可以看作是 Context Engineering 的上位概念：
- Context Engineering 聚焦在「給 LLM 什麼 context」
- Harness Engineering 更廣泛，包含 context + workflow + feedback loop + evaluation

### 跟 Hermes Agent 的關係
Hermes 的 Closed Learning Loop 就是 Harness Engineering 的實作：
- 自動建立 skill documents = 自動學會如何 harness 特定任務
- MEMORY.md = 累積的 harness 策略

## 備註
- 1:25:50 提到 Anthropic Haiku 3.5 API 已退役，實驗使用 Open Router 的服務

## 對 areomoon 的意義
1. Harness Engineering 是你在 Material Science Agent 工作中最核心的技能
2. 你的 extraction agent 本質上就是在「harness」LLM 做材料論文 extraction
3. 李宏毅教授是台灣 AI 教育的標竿人物，他的課程系列值得全部看完
4. 這些講座可以加入 areomoon_agent_warmup 的學習資源

## 參考資源
- 影片：https://www.youtube.com/watch?v=R6fZR_9kmIw
- 李宏毅頻道：https://www.youtube.com/@HungyiLeeNTU
