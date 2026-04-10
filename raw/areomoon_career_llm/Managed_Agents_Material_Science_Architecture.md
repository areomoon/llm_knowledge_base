# Managed Agents × Material Science Agent 架構設計

**文件狀態**: Draft v1.0  
**作者**: areomoon  
**日期**: 2026-04-10  
**適用對象**: Material Science Extraction Agent 算法工程師（入職後 team review 用）

---

## 目錄

1. [文件目的](#1-文件目的)
2. [背景與驅動因素](#2-背景與驅動因素)
3. [系統架構](#3-系統架構)
4. [ACE Framework Mapping](#4-ace-framework-mapping)
5. [三階段 Rollout Plan](#5-三階段-rollout-plan)
6. [Key Design Decisions](#6-key-design-decisions)
7. [與現有系統的對比](#7-與現有系統的對比)
8. [風險與緩解](#8-風險與緩解)
9. [Success Metrics](#9-success-metrics)
10. [First 30 Days Action Plan](#10-first-30-days-action-plan)

---

## 1. 文件目的

本文件為即將到來的 **Material Science Extraction Agent 算法工程師**角色，設計一套基於 **Claude Managed Agents**（Anthropic 的 production-grade agent 執行環境）的系統架構藍圖。

目標是：**不從零建 agent harness，而是利用 Managed Agents 的基礎設施，將工程重心放在 memory store 設計、custom tools、和 extraction playbook 的演化邏輯上。**

本文件期望達成：
- 提供一個可直接交給 team 討論的架構草案
- 建立從 onboarding Week 1 到 Week 7+ 的技術路徑
- 作為在面試或早期入職階段展示系統思維的具體 artifact

---

## 2. 背景與驅動因素

### 2.1 材料科學 Extraction Agent 的核心挑戰

材料科學論文是 LLM agent 面對最難的資料來源之一，原因來自四個維度：

**Multi-modal 複雜性**
- 論文包含：PDF 文字、HTML table（含合併欄位）、XRD 圖譜、SEM/TEM 影像、化學式（A₂BO₄ 格式）、單位混用（S/cm vs mS/m）
- 每種 modality 需要不同的 extraction 策略，且策略本身會隨論文類型而變

**Domain-specific 知識密度**
- 「BaTiO₃ 的居里溫度約 120°C」這類知識既非 common knowledge，也難以從上下文推斷
- 錯誤的 extraction 若未被驗證，會污染下游的材料數據庫
- 需要 domain knowledge 來判斷 reported value 是否合理（e.g., ZT > 3 在目前技術水準下可疑）

**長時間運算反饋循環**
- DFT 計算可能耗時數小時到數天
- 跨論文的 cross-validation 需要 agent 在多個 session 之間保持記憶
- 單次 extraction session 可能需要處理 50-100 頁的長文件

**Ground Truth 昂貴**
- 標準的 supervised fine-tuning 需要大量人工標注的 (paper → structured JSON) 對
- 材料科學專家的時間成本極高，annotation bandwidth 有限
- 需要一種**不完全依賴標注資料**的改進機制

### 2.2 為什麼選 Managed Agents 而不是自建 Harness

傳統路徑是用 LangChain / LangGraph / AutoGen 自建 agent harness。這條路的問題在 2026 年已經相對清楚：

| 問題 | 自建 Harness | Managed Agents |
|------|-------------|----------------|
| Context 管理 | 自行實作 compression、memory overflow 處理 | 平台層處理（Claude Code 的三層壓縮已成熟） |
| Tool lifecycle | 手動管理 tool registration、permission gating | 內建 PreToolUse/PostToolUse hooks |
| Multi-agent 協調 | 自行設計 mailbox pattern、fan-out | Managed Agents 提供 agent spawning API |
| Memory persistence | 需要自行選擇 vector store vs file store | Memory store API 原生支援 |
| 基礎設施維護成本 | 高（需要維護 harness 本身）| 低（focus on domain logic） |

更關鍵的是：**Claude Code 的 leak source 分析顯示，production agent 的 90% 工程量在 harness，不在 reasoning loop。** 如果平台已經解決了 harness，我們的工程時間應該花在材料科學的 domain logic 上。

### 2.3 2026 年的技術環境

Anthropic 在 2025-2026 年間，將 Claude Code 的架構知識（三層記憶、scoped rules、context compression、permission gating）轉化為 **Claude Managed Agents** managed product。這是一個明確的技術訊號：

- ACE Framework（Stanford/SambaNova，2025）的學術研究已驗證「evolving playbook 取代 fine-tuning」的可行性
- Managed Agents 的 memory store API 直接支援 ACE 的 Generator/Reflector/Curator 模式
- 2026 年的 materials AI 競爭點，已從「能不能建 agent」轉移到「能不能讓 agent 持續改進」

---

## 3. 系統架構

### 3.1 高層架構圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                                   │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐│
│  │  PDF     │  │  HTML    │  │  Images  │  │  Dataset / JSON      ││
│  │ (論文)   │  │ (article)│  │(SEM/XRD) │  │  (Materials Project) ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘│
│       └─────────────┴──────────────┴────────────────────┘           │
│                           │                                          │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  MANAGED AGENTS LAYER                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Agent Session                                                 │ │
│  │                                                                │ │
│  │  model: claude-opus-4-6 (or claude-sonnet-4-6 for speed)      │ │
│  │  environment: Python 3.11 + PyMuPDF + RDKit + ase + matminer  │ │
│  │                                                                │ │
│  │  ┌──────────────────────────────────────────────────────────┐ │ │
│  │  │  SYSTEM PROMPT (動態組裝)                                │ │ │
│  │  │  [1] Global extraction instructions (cached)            │ │ │
│  │  │  [2] Domain rules from materials_domain_knowledge       │ │ │
│  │  │  [3] Current extraction playbook (from memory store)    │ │ │
│  │  │  [4] Session state (paper metadata, target fields)      │ │ │
│  │  └──────────────────────────────────────────────────────────┘ │ │
│  │                                                                │ │
│  │  Tools (progressive discovery):                                │ │
│  │  ┌───────────┐ ┌───────────┐ ┌────────────┐ ┌─────────────┐  │ │
│  │  │  bash     │ │read/write │ │ glob/grep  │ │  web_fetch  │  │ │
│  │  └───────────┘ └───────────┘ └────────────┘ └─────────────┘  │ │
│  │  ┌─────────────────────┐ ┌──────────────────────────────────┐ │ │
│  │  │materials_property_  │ │ structure_visualizer             │ │ │
│  │  │lookup               │ │ (3D crystal/molecular vis)       │ │ │
│  │  └─────────────────────┘ └──────────────────────────────────┘ │ │
│  │  ┌─────────────────────┐ ┌──────────────────────────────────┐ │ │
│  │  │unit_conversion      │ │ citation_tracker                 │ │ │
│  │  └─────────────────────┘ └──────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     MEMORY LAYER                                     │
│                                                                      │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│  │  materials_domain_knowledge  │  │  extraction_playbook         │ │
│  │  (READ-ONLY)                 │  │  (READ-WRITE)                │ │
│  │                              │  │                              │ │
│  │  - 晶體結構規則               │  │  - 模態別抽取策略              │ │
│  │  - 合成條件約束               │  │  - 已知困難案例的解法          │ │
│  │  - 單位換算標準               │  │  - Anti-patterns             │ │
│  │  - 材料分類 ontology          │  │  - 信心度校準規則              │ │
│  │  - 安全約束（有害材料）         │  │  版本: v1.0, v1.1, ...      │ │
│  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                      │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐ │
│  │  extraction_cases            │  │  user_feedback               │ │
│  │  (READ-WRITE)                │  │  (READ-WRITE)                │ │
│  │                              │  │                              │ │
│  │  - paper_id + field →        │  │  - reviewer 修正記錄          │ │
│  │    extracted_value +         │  │  - flagged errors            │ │
│  │    confidence + method       │  │  - preferred format samples  │ │
│  │  - validation_result         │  │  - domain expert annotations │ │
│  │  - curator_notes             │  │                              │ │
│  └──────────────────────────────┘  └──────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                                    │
│                                                                      │
│  ┌─────────────────┐  ┌────────────────────┐  ┌──────────────────┐  │
│  │  Structured JSON │  │  Markdown Report   │  │  Visualization   │  │
│  │                  │  │                    │  │                  │  │
│  │  {               │  │  ## Extraction     │  │  Crystal struct  │  │
│  │    "material":   │  │  Summary           │  │  (3D render)     │  │
│  │    "property":   │  │  - confidence map  │  │                  │  │
│  │    "value":      │  │  - review flags    │  │  Property chart  │  │
│  │    "confidence": │  │  - provenance      │  │  (matplotlib)    │  │
│  │    "provenance": │  │                    │  │                  │  │
│  │    "flags": []   │  │                    │  │                  │  │
│  │  }               │  │                    │  │                  │  │
│  └─────────────────┘  └────────────────────┘  └──────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Environment 配置

```python
# Managed Agents 環境定義（概念性 pseudocode）
agent = ManagedAgent(
    model="claude-opus-4-6",
    environment={
        "python_version": "3.11",
        "packages": [
            "pymupdf",          # PDF 解析（比 pypdf 更穩定的 table extraction）
            "rdkit",            # 化學式解析、SMILES 處理
            "ase",              # Atomic Simulation Environment（晶體結構操作）
            "matminer",         # 材料特性特徵化
            "pymatgen",         # Materials Project 整合
            "pillow",           # 圖片前處理
            "camelot-py",       # PDF table extraction（處理合併欄位）
            "pint",             # 物理量單位自動換算
        ]
    },
    memory_stores=[
        MemoryStore("materials_domain_knowledge", access="read"),
        MemoryStore("extraction_playbook", access="read_write"),
        MemoryStore("extraction_cases", access="read_write"),
        MemoryStore("user_feedback", access="read_write"),
    ],
    tools=[
        "bash", "read", "write", "glob", "grep", "web_fetch",
        "materials_property_lookup",  # custom
        "structure_visualizer",       # custom
        "unit_conversion",            # custom
        "citation_tracker",           # custom
    ],
    permission_policy={
        "bash": "prompt",           # 需要確認才執行 shell 命令
        "write": "prompt",          # 寫入前確認
        "web_fetch": "allow",       # 查詢 Materials Project API 不需確認
        "read": "allow",
    }
)
```

### 3.3 Memory Layer 詳細設計

Memory store 是本架構最關鍵的設計決策，直接對應 ACE 的 evolving playbook 機制。

#### `materials_domain_knowledge`（唯讀，人工維護）

```markdown
# Materials Domain Knowledge Store

## Crystal Structure Rules
- ABO₃ perovskites: A-site 通常為大離子（Ba, Sr, La），B-site 為小離子（Ti, Mn, Fe）
- 報告 lattice parameter 時，如未指定溫度，預設為室溫（~298K）
- Layered structures (Ruddlesden-Popper series: Aₙ₊₁BₙO₃ₙ₊₁) 的 n 值決定層數

## Synthesis Condition Constraints
- 固態反應法：煅燒溫度通常 800-1200°C，燒結溫度高於煅燒 100-300°C
- 水熱合成：通常 120-250°C，0.5-48h，pH 調控形貌
- 如報告溫度 > 2000°C 且為氧化物，需標記為 flag（可能為 SPS/spark plasma sintering）

## Unit Standards
- 電導率: S/cm（若報告為 Ω⁻¹cm⁻¹，等價；若為 S/m 需除以 100）
- 熱電優值 ZT: 無量綱，合理範圍 0.01-3.5（>3 需 flag）
- 磁化強度: emu/g 或 Am²/kg（換算係數 1 emu/g = 1 Am²/kg）

## Material Classification Ontology
- 按功能: thermoelectric / ferroelectric / multiferroic / superconductor / battery material / ...
- 按結構: perovskite / spinel / garnet / layered / amorphous / ...
- 按合成法: solid-state / sol-gel / hydrothermal / CVD / MBE / ...

## Safety Constraints
- 含 Pb 材料: 需在 extraction output 標記 [HAZARDOUS: Pb]
- 含 Cd、Hg、As、Cr(VI): 同上，標記對應元素
- 放射性元素（U、Th）: 需要特殊處理標記
```

#### `extraction_playbook`（讀寫，Curator 自動更新）

```markdown
# Extraction Playbook v1.3
# Last updated: 2026-04-10
# Curator: session-{id}

## Table Extraction Rules
- [P-001] 當 table header 跨越多行時，先重建完整 header，再逐行 parse
- [P-002] 「N/A」「-」「—」均視為 missing value，不填 0
- [P-003] 含 superscript 的數值（e.g., 1.5 × 10³）需展開為浮點數後再存儲

## Figure Extraction Rules
- [P-010] XRD 圖譜：2θ 峰位精確到 ±0.05°；只報告主峰，不報告雜質峰（除非文中明確討論）
- [P-011] SEM 影像：報告形貌描述（rod/sphere/plate/irregular），若 scale bar 可讀則報告粒徑範圍

## Confidence Calibration
- [P-020] 從 Abstract/Conclusion 抽取的值信心度 ×0.9（可能為近似值）
- [P-021] 從 Table 抽取的值信心度 ×1.0（結構化，最可靠）
- [P-022] 從 Figure 估讀的值信心度 ×0.7

## Anti-patterns
- [AP-001] 不要把 theoretical/calculated 值和 experimental 值混用同一個 field
- [AP-002] 不要根據材料名稱猜測 composition（Fe₃O₄ ≠ FeO + Fe₂O₃ 的混合）
- [AP-003] Review articles 的值通常是 median/average，不是原始測量值

## Domain-specific Edge Cases
- [EC-001] ZnO 的電導率會隨環境大氣（O₂ vs N₂）大幅變化，需記錄測量環境
```

#### `extraction_cases`（讀寫，每次 extraction 後寫入）

```json
{
  "case_id": "case-2026-04-10-001",
  "paper_doi": "10.1021/acs.nanolett.5b04580",
  "paper_title": "High ZT Thermoelectric via Band Engineering in PbTe",
  "extraction_result": {
    "material": "Pb₀.₉₈Na₀.₀₂Te",
    "property": "ZT",
    "value": 1.8,
    "temperature": "500K",
    "confidence": 0.92,
    "source_location": "Figure 3a",
    "extraction_method": "figure_reading"
  },
  "validation": {
    "self_consistency_check": "pass",
    "database_validation": "consistent_with_materials_project",
    "cross_doc_validation": "not_checked"
  },
  "curator_notes": "ZT 值從 Figure 3a 估讀，使用 playbook rule P-022 (×0.7 confidence) 但後以數字形式出現在 Table 2，已升級為 P-021 (×1.0)。新規則候選：圖中有文字標注的值信心度可升級。"
}
```

### 3.4 Custom Tools 規格

#### `materials_property_lookup`

```python
def materials_property_lookup(
    formula: str,
    property: str,  # "band_gap" | "density" | "elastic_modulus" | ...
    structure_type: str = None,
) -> dict:
    """
    查詢 Materials Project API (mp-api) 獲取已知材料的參考值。
    用於 extraction validation：比對 extracted value 與已知值的偏差。
    
    Returns:
    {
        "mp_id": "mp-19770",
        "formula": "BaTiO3",
        "property": "band_gap",
        "value": 1.78,  # eV, GGA calculated
        "source": "Materials Project",
        "warning": "GGA tends to underestimate band gaps by ~40%"
    }
    """
    from mp_api.client import MPRester
    with MPRester(api_key=os.environ["MP_API_KEY"]) as mpr:
        docs = mpr.summary.search(
            formula=formula,
            fields=["material_id", "formula_pretty", property]
        )
    return _format_result(docs, property)
```

#### `unit_conversion`

```python
def unit_conversion(
    value: float,
    from_unit: str,
    to_unit: str,
    quantity_type: str,  # "electrical_conductivity" | "thermal_conductivity" | ...
) -> dict:
    """
    使用 pint 進行材料科學常用單位換算。
    特殊處理材料科學中的非標準單位（e.g., emu/g, ZT 無量綱）。
    
    Returns:
    {
        "original": {"value": 1.5, "unit": "S/cm"},
        "converted": {"value": 150, "unit": "S/m"},
        "factor": 100,
        "notes": "Standard SI for electrical conductivity is S/m"
    }
    """
    import pint
    ureg = pint.UnitRegistry()
    # ... 材料科學特殊換算邏輯
```

#### `structure_visualizer`

```python
def structure_visualizer(
    formula: str = None,
    cif_path: str = None,
    mp_id: str = None,
    output_format: str = "png",  # "png" | "html" | "ascii"
) -> str:
    """
    生成晶體/分子結構的視覺化。
    優先級: cif_path > mp_id > formula（formula 會搜 Materials Project 取第一個匹配）
    
    Returns: 輸出文件的路徑
    """
    from pymatgen.core import Structure
    from pymatgen.vis.structure_vtk import StructureVis
    # ... 視覺化邏輯
```

#### `citation_tracker`

```python
def citation_tracker(
    paper_doi: str,
    action: str,  # "get_references" | "find_citing_papers" | "get_coauthors"
) -> dict:
    """
    追蹤論文引用關係，用於 cross-document validation。
    如果 paper A 的 ZT=2.1 被 paper B 引用並報告為 ZT=2.0，
    citation_tracker 可以找到這個連結。
    
    Returns:
    {
        "doi": "10.1021/...",
        "references": [...],
        "cited_by": [...],
        "semantic_scholar_id": "..."
    }
    """
    # 使用 Semantic Scholar API（免費，無需 API key）
    import requests
    resp = requests.get(
        f"https://api.semanticscholar.org/graph/v1/paper/{paper_doi}",
        params={"fields": "references,citations"}
    )
    return resp.json()
```

---

## 4. ACE Framework Mapping

ACE（Agentic Context Engineering，Stanford/SambaNova 2025）的 Generator/Reflector/Curator 三角色，在本架構中有精確的映射：

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ACE GRC 循環                                      │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    GENERATOR                                 │   │
│   │                                                              │   │
│   │  = Session 本身的推理循環                                    │   │
│   │                                                              │   │
│   │  1. 讀取 system prompt（含 domain knowledge + playbook）     │   │
│   │  2. 制定 extraction plan（per modality：text/table/figure）  │   │
│   │  3. 執行 tools（bash, read, materials_property_lookup...）   │   │
│   │  4. 生成 structured JSON draft + confidence scores          │   │
│   │  5. Flag 困難欄位（merged cells, ambiguous units...）        │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │ extraction draft                      │
│                              ▼                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    REFLECTOR                                 │   │
│   │                                                              │   │
│   │  = 每次 extraction 完成後的 self-consistency check           │   │
│   │                                                              │   │
│   │  1. Self-consistency: 以 3 種不同 prompt 重跑 extraction，   │   │
│   │     比較關鍵欄位的一致性（disagreement → flag）              │   │
│   │  2. Database validation: 對比 Materials Project 已知值       │   │
│   │     （偏差 > 20% → flag + 記錄偏差方向）                    │   │
│   │  3. Internal consistency: 如 composition + density 不匹配   │   │
│   │     → 其中一個有誤                                          │   │
│   │  4. Cross-doc validation: 查 citation_tracker 找相同材料的  │   │
│   │     其他報告，比較數值範圍                                   │   │
│   └──────────────────────────┬──────────────────────────────────┘   │
│                              │ lessons + anomalies                   │
│                              ▼                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    CURATOR                                   │   │
│   │                                                              │   │
│   │  = Memory store 的 write/update 操作                        │   │
│   │                                                              │   │
│   │  Input: Reflector 的 lessons + anomalies                    │   │
│   │                                                              │   │
│   │  Actions:                                                    │   │
│   │  - 寫入 extraction_cases（本次 extraction 的完整記錄）       │   │
│   │  - 如發現新的 extraction pattern → append to playbook       │   │
│   │  - 如發現現有 playbook rule 有誤 → update rule              │   │
│   │  - 如 user_feedback 有新的 correction → 提取 rule candidate │   │
│   │  - 週期性 de-duplication（playbook 每 50 cases 觸發一次）   │   │
│   │                                                              │   │
│   │  Constraint: Curator 寫入 playbook 前，先計算 rule 的        │   │
│   │  支持案例數（n < 3 → 標記為 tentative，不強制執行）          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              │ updated playbook                      │
│                              ▼                                       │
│                    下一次 session 使用更新後的 playbook              │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.1 Evolving Playbook 詳細機制

Playbook 的演化遵循 ACE 的 **Grow-and-Refine** 算法：

```
新的 extraction lesson
    ↓
[Curator: 判斷是否為新規則]
    │
    ├── 是新 pattern → append as [P-NNN] tentative
    │
    ├── 與現有 rule 相關 → semantic similarity check
    │       │
    │       ├── 相似度 > 0.85 → merge into existing rule
    │       └── 相似度 < 0.85 → append as new rule
    │
    └── 與現有 rule 矛盾 → counter-evidence check
            │
            ├── n(support) < n(counter) → deprecate old rule
            └── n(support) > n(counter) → flag as edge case
```

**Playbook 版本控制**：每次 Curator 修改 playbook，都記錄版本號、觸發的 case_id、修改摘要。版本控制使 rollback 可行（見第 8 節）。

---

## 5. 三階段 Rollout Plan

### Phase 1: Infrastructure Setup（Week 1-2）

**目標**: 建立可運行的最小系統，跑通第一個 extraction。

**Week 1**:
- Day 1-2: 閱讀 Managed Agents quickstart，建立 development session
  - 驗證 Python 3.11 + PyMuPDF + matminer 環境可用
  - 測試 `materials_property_lookup` tool 能成功查詢 Materials Project API
- Day 3-4: 設計並初始化四個 memory store
  - `materials_domain_knowledge`: 從 MatKG、OPTIMADE vocabulary 手動整理初始版本（~50 條規則）
  - `extraction_playbook`: 從現有材料抽取文獻中整理初始 playbook v0.1（~20 條規則）
  - `extraction_cases`: 空 store，定義 schema
  - `user_feedback`: 空 store，定義 schema
- Day 5: 跑第一個 extraction session
  - 選一篇已知 ground truth 的論文（Materials Project 有收錄的材料）
  - 手動比對 extracted values vs ground truth

**Week 2**:
- Day 6-8: 建立 Reflector 的 self-consistency check 流程
  - 實作 3x extraction + comparison 邏輯
  - 定義 disagreement threshold（e.g., 數值欄位差異 > 10% 觸發 flag）
- Day 9-10: 建立 Curator 的 playbook write 流程
  - 跑 3-5 篇測試論文，觀察哪些 extraction 困難
  - 手動整理 lessons，寫入 playbook
  - 驗證 playbook 的更新確實影響下一次 extraction

**Deliverable**: 可以跑通一個完整 GRC 循環的 demo session（不需要高準確率，只需流程完整）

---

### Phase 2: Playbook Seeding（Week 3-6）

**目標**: 建立 50+ cases 的積累，讓 playbook 到達第一個 stable version。

**Week 3-4: Benchmark Paper Set**
- 選 20 篇有完整 supplementary data 的論文（ground truth 可靠）
- 類型覆蓋：perovskite / thermoelectric / battery / thin film（4 種 domain）
- 每篇論文跑完後，由人工確認 extraction 結果並寫入 user_feedback

**Week 5-6: Playbook Refinement**
- 分析 20 篇 cases 的 Reflector flags，找出高頻錯誤模式
- 集中更新 playbook 的 Table Extraction Rules 和 Confidence Calibration
- 建立 **regression test set**：每次 playbook 更新後，重新跑這 20 篇，確保沒有退步

**Metrics for Phase 2 Exit**:
- Extraction precision ≥ 0.75（benchmark set）
- Playbook 達到 v0.5（≥ 30 條 confirmed rules）
- 每篇論文平均 extraction time < 5 分鐘

---

### Phase 3: Evolving Playbook + RLPR（Week 7+）

**目標**: 啟動自動化的 playbook evolution，並評估 RLPR fine-tuning 的可行性。

**Week 7-8: Automated Curator**
- 將 Curator 的 playbook write 邏輯自動化
  - 每次 session 結束，自動觸發 Curator pass
  - Curator 的 rule 候選需要 n ≥ 3 個 supporting cases 才寫入 confirmed rules
- 建立 playbook health dashboard（新規則增長率、rule 使用頻率、conflict 率）

**Week 9-12: RLPR 評估**

RLPR（Reinforcement Learning from Playbook Reflection）是 Phase 3 的核心 research 問題：

```
Question: 當 extraction_cases 累積到 N 個（N = 100? 500?），
用這些 cases 做 SFT + RLHF 是否比持續 memory update 更有效？

Experiment Design:
- Control: playbook-only（持續更新 memory，不 fine-tune）
- Treatment: SFT on accumulated cases → fine-tuned model
- Evaluation: benchmark set precision/recall
- Hypothesis: playbook 在 interpretability 上勝，fine-tuning 在 generalization 上勝
```

在此階段，這是一個 research question，不是既定方案。實際執行取決於 cases 積累速度和標注品質。

**Deliverable**: 能每日自動處理 10+ 篇新論文，playbook 持續演化，precision > 0.85

---

## 6. Key Design Decisions

### 6.1 為什麼用 Memory Store 取代 Fine-tuning

| 維度 | Memory Store | Fine-tuning |
|------|-------------|-------------|
| **成本** | API call 成本（低，一次 write 幾分鐘） | GPU 計算成本（高，$100-$10,000+/run） |
| **迭代速度** | 即時（Curator 寫入後下一個 session 生效） | 慢（需要 dataset prep → 訓練 → 評估）|
| **可解釋性** | 高（playbook 是人可讀的 markdown） | 低（weight 變化不透明）|
| **回滾** | 容易（版本控制 playbook，rollback = 載入舊版本） | 困難（需要重訓或保留 checkpoint）|
| **適合的知識類型** | Explicit, interpretable rules | Statistical patterns over large data |

**結論**: 在 cases 數量 < 1000 的早期階段，memory store 幾乎在所有維度勝出。Fine-tuning 作為 Phase 3 的可能補充，而非替代。

### 6.2 Custom Tools vs MCP Server

| 場景 | 建議方案 | 理由 |
|------|---------|------|
| Materials Project API 查詢 | Custom tool | 單一 session 內使用，不需要跨 project 共享 |
| 圖形化視覺化（一次性輸出）| Custom tool | 輕量、不需要狀態管理 |
| 公司內部資料庫連接 | MCP Server | 跨多個 agent/project 複用，值得建 server |
| 大型 HPC 作業調度（未來）| MCP Server | 複雜的連接管理，需要專用 server |

**Rule of thumb**: 單一 agent 用 ≤ 3 次的工具用 custom；需要跨 project 複用或有複雜狀態管理的用 MCP。

### 6.3 Memory Sharding Strategy

四個 memory store 的切分邏輯：

```
materials_domain_knowledge
    → 靜態、人工維護、高信心度的領域知識
    → 類比於教科書
    → 更新頻率：每季度，需要 domain expert 審核

extraction_playbook
    → 動態、Curator 更新的 extraction 策略
    → 類比於 SOP（Standard Operating Procedure）
    → 更新頻率：每 session（自動），每週（人工驗證）

extraction_cases
    → 每次 extraction 的詳細記錄（輸入、輸出、驗證結果）
    → 類比於 lab notebook
    → 更新頻率：每次 extraction 後立即寫入

user_feedback
    → Reviewer 的修正和偏好
    → 類比於 code review comments
    → 更新頻率：reviewer 看完結果後寫入
```

**為什麼不合並成一個 store？** 讀取粒度不同。每個 session 都需要讀取 playbook 和 domain knowledge，但 extraction_cases 太大，只在 Curator 比對時才讀。分開存儲確保 context window 不被淹沒。

### 6.4 Versioning + Rollback Strategy

```
Playbook Versioning 機制:

playbook_v1.0.md    ← 手動建立的初始版本（Week 2）
playbook_v1.1.md    ← Curator 在 case-050 後的自動更新
playbook_v1.2.md    ← Curator 在 case-100 後的自動更新（de-duplication pass）
playbook_v1.3.md    ← 人工 review 後的修訂版

每個版本文件包含:
- version: v1.3
- updated_at: 2026-05-01
- trigger: case-case-2026-05-01-143 (Curator auto) / manual review
- changes: [P-025 updated, P-030 added, P-018 deprecated]
- n_rules: 45
- n_confirmed: 38 / n_tentative: 7
```

**Rollback 觸發條件**:
1. Benchmark set precision 下降超過 5%
2. 連續 10 個 sessions 的 Reflector flags 比例上升
3. Domain expert 審核後判定 playbook 有系統性偏誤

**Rollback 操作**:
```python
# 回滾到特定版本只需要:
agent.load_memory_store("extraction_playbook", version="v1.1")
# 所有後續 sessions 自動使用 v1.1
```

---

## 7. 與現有系統的對比

### 7.1 三系統對比矩陣

| 維度 | MARS（19 agents）| LLMatDesign | 本方案（Managed Agents）|
|------|-----------------|-------------|------------------------|
| **架構重量** | 重（19 agents + 16 tools）| 輕 | 中（1 agent + 4 memory + 4 custom tools）|
| **基礎設施複雜度** | 高（19 個 agent 需要協調）| 低 | 低（Managed Agents 處理 harness）|
| **Persistent Learning** | 無（session 間不保留策略）| 有（strategy library）| 有（extraction_playbook）|
| **Multi-modal Extraction** | 有（部分）| 無 | 有（核心 use case）|
| **可解釋性** | 中（specialist agents 有角色，但 no playbook）| 高（strategy library 可讀）| 高（playbook 是人可讀 markdown）|
| **上手成本** | 高（需要理解 19 個 agent 的交互）| 低 | 低（Managed Agents quickstart）|
| **適合場景** | 閉環 discovery（從假設到實驗）| 材料設計 | 文獻 extraction + knowledge base building |

### 7.2 選擇本方案的理由

**MARS 不適合的原因**:
- MARS 是 discovery-first 系統，最強的點在 Hypothesis Generator + DFT Calculator 的閉環
- 我們的核心任務是 **extraction**（從論文中結構化數據），不是提出新材料
- 19 個 agents 的協調成本，對一個入職工程師來說是不必要的複雜度

**LLMatDesign 的策略庫**:
- LLMatDesign 的 strategy library 是最接近 ACE playbook 的設計
- 但它缺乏 multi-modal extraction 能力（無法處理 XRD 圖、SEM 影像）
- 本方案保留了 strategy library 的核心理念，並將其延伸到 extraction domain

**本方案的差異化**:
```
本方案 = LLMatDesign 的 persistent strategy library
       + MARS 的 multi-modal 能力
       + Managed Agents 的 harness（取代自建 LangGraph）
       + ACE 的 GRC 自動演化機制
```

---

## 8. 風險與緩解

### 8.1 Beta Feature Risk

**風險**: Managed Agents 目前（2026-04）為 beta，API 可能在未來版本中變動。

**緩解措施**:
- 將 Managed Agents API 呼叫封裝在 adapter layer，避免直接散布在業務邏輯中
- 訂閱 Anthropic changelog，設置 breaking change 警報
- 每個月跑一次 compatibility check（跑 benchmark set，確認行為不變）
- Phase 1 同時準備 fallback 方案：如果 Managed Agents API 大改，能在 2 週內切換到 vanilla Claude API + 自建 memory file 系統

### 8.2 Memory Pollution

**風險**: 一批品質差的 extraction cases 觸發 Curator，寫入錯誤的 playbook rules，導致後續 extraction 系統性偏誤。

**緩解措施**:
1. **Tentative rules 機制**: 新規則在 n ≥ 3 supporting cases 前都標記為 tentative，不強制執行
2. **Rollback 機制**: playbook 版本控制（見 6.4），benchmark set 回歸檢測
3. **Curator confidence gate**: Curator 對 playbook 的任何修改，都需要評估 confidence score > 0.8 才執行
4. **Monthly human review**: 每個月 domain expert 審核 playbook 的新增規則（~10-15 條/月）

```
Memory Pollution 防護層:

[自動層]  Curator confidence gate (>0.8)
    ↓
[自動層]  Tentative rule 機制（n ≥ 3 才 confirm）
    ↓
[自動層]  Benchmark regression check（每次 playbook 更新後跑）
    ↓
[人工層]  Monthly domain expert review
    ↓
[人工層]  Emergency rollback（如 precision 下降 > 5%）
```

### 8.3 Cost Estimation

基於 claude-opus-4-6 的 API 呼叫成本估算：

| 操作 | Token 估算 | 頻率 | 月成本估算 |
|------|-----------|------|----------|
| Single paper extraction（含 Reflector 3x runs）| ~50K tokens in + ~10K tokens out | 50 papers/month | ~$60 |
| Curator pass（讀取 cases + 更新 playbook）| ~20K tokens | 50 sessions/month | ~$15 |
| Playbook de-duplication（月度）| ~30K tokens | 1x/month | ~$3 |
| **Total（Phase 2）** | | | **~$80/month** |

**Note**: 使用 claude-sonnet-4-6 可以將成本降低到 ~$20/month，但準確率可能下降 10-15%。建議 Phase 1-2 用 Opus 建立基準，Phase 3 評估是否切換到 Sonnet。

### 8.4 Compliance

**材料專利風險**:
- 部分論文中的合成方法可能涉及專利
- extraction 的結果是結構化數據，不是論文原文複製 → 通常在 fair use 範圍
- 但如果要對外提供 API 服務，需要法律確認

**商業機密風險**:
- 公司內部論文和客戶論文需要與 Anthropic API 的資料使用政策確認
- 建議為內部/機密論文建立 local inference 選項（e.g., self-hosted Llama 4）

**有害材料**:
- `materials_domain_knowledge` 中已建立安全標記（Pb, Cd, Hg, U 等）
- 所有含有害元素的 extraction result 自動加入警告標記

---

## 9. Success Metrics

### 9.1 Extraction Quality

| Metric | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|---------------|---------------|----------------|
| Property value precision | ≥ 0.60 | ≥ 0.75 | ≥ 0.85 |
| Property value recall | ≥ 0.50 | ≥ 0.70 | ≥ 0.80 |
| Unit correctness | ≥ 0.90 | ≥ 0.95 | ≥ 0.98 |
| Confidence calibration (ECE) | - | < 0.15 | < 0.10 |

**Benchmark set**: 選擇 20 篇有完整 supplementary data 且 Materials Project 有收錄的論文，人工標注作為 ground truth。

### 9.2 System Performance

| Metric | Target | 備註 |
|--------|--------|------|
| Per-paper extraction time | < 5 min | 含 3x Reflector runs |
| Playbook update cycle | < 1 min | Curator pass |
| Memory store read latency | < 2s | 在 session 啟動時 |

### 9.3 Playbook Health

| Metric | Description | Target |
|--------|-------------|--------|
| Playbook growth rate | 每週新增的 confirmed rules | 3-8 rules/week（Phase 2）|
| Rule utilization rate | 被 session 實際查詢到的 rule 比例 | > 60%（低表示 playbook 太泛）|
| Conflict rate | Curator 偵測到互相矛盾的 rules 比例 | < 5% |
| Rollback frequency | 需要 rollback 的次數 | 0/month（理想）|

### 9.4 Time-to-Value

| Milestone | Target Date（相對於入職）| 描述 |
|-----------|------------------------|------|
| First working extraction | Week 1, Day 5 | 一篇論文的完整 extraction |
| Demo-able system | Week 2, Day 10 | 可以給 team 展示的 GRC 循環 |
| Stable benchmark precision > 0.75 | Week 6 | Phase 2 exit criteria |
| Production-ready（> 0.85）| Week 12 | Phase 3 target |

---

## 10. First 30 Days Action Plan

### Week 1: 環境與基礎設施

| Day | 任務 | 預期產出 |
|-----|------|---------|
| 1 | 閱讀 Managed Agents documentation；確認 API access；安裝 Python 環境 | 可運行的 dev environment |
| 1 | 閱讀 wiki/concepts/ace-framework.md、material-science-agents.md、agentic-harness.md | 理解理論基礎 |
| 2 | 初始化四個 memory stores；設計 extraction_cases 的 JSON schema | memory store 基礎架構 |
| 2 | 整理 `materials_domain_knowledge` 初始版本（從 MatKG + OPTIMADE vocabulary） | domain knowledge v0.1 |
| 3 | 實作 `materials_property_lookup` custom tool；測試 Materials Project API 連通 | working tool |
| 3 | 實作 `unit_conversion` tool；覆蓋主要材料科學單位 | working tool |
| 4 | 建立 extraction playbook v0.1（手動整理 ~20 條初始規則） | playbook v0.1 |
| 4 | 建立 system prompt 模板（static instructions + dynamic memory loading） | system prompt v0.1 |
| 5 | 跑第一個 extraction session（選一篇有已知 ground truth 的論文） | first extraction result |
| 5 | 手動執行 Reflector check；記錄發現的問題 | first Reflector report |

### Week 2: Reflector 與初步 Curator

| Day | 任務 | 預期產出 |
|-----|------|---------|
| 6 | 實作 3x self-consistency check 邏輯 | automated Reflector |
| 6 | 定義 disagreement threshold 和 flag 格式 | Reflector v0.1 |
| 7 | 實作 database validation（對比 Materials Project）| validation pipeline |
| 8 | 手動執行 Curator pass for Week 1 results；將 lessons 寫入 playbook | playbook v0.2 |
| 8 | 確認 playbook 更新後，下一個 session 的行為有所改變 | GRC loop 驗證 |
| 9 | 實作 extraction_cases 的自動寫入（session 結束後觸發）| automated case logging |
| 9 | 設計 user_feedback store 的填寫流程（給 reviewer 用的 UI 或 template）| feedback interface |
| 10 | 完整跑通 5 篇測試論文；記錄 precision/recall | Week 2 metrics |
| 10 | 準備 team demo（10 分鐘）：展示 GRC 循環的一個完整例子 | demo ready |

### Week 3-4: Benchmark Building

| 任務 | 預期產出 |
|------|---------|
| 選定 20 篇 benchmark 論文（4 種材料類型 × 5 篇，有完整 ground truth）| benchmark set v1 |
| 對 benchmark set 跑完整 extraction，人工標注結果 | annotated cases |
| 計算 Phase 1 baseline metrics（precision/recall/unit accuracy）| baseline metrics |
| 整理 top 10 high-frequency extraction errors，更新 playbook | playbook v0.3 |
| 實作 `structure_visualizer` tool | working tool |
| 實作 `citation_tracker` tool | working tool |

### Week 5-6: Playbook Seeding + Exit Criteria

| 任務 | 預期產出 |
|------|---------|
| 跑完 benchmark set 的第二輪 extraction（使用更新後的 playbook）| second-pass metrics |
| 比較 precision/recall 的改善幅度 | iteration improvement data |
| 將 playbook 精煉到 v0.5（≥ 30 條 confirmed rules，< 5 個 conflicts）| stable playbook v0.5 |
| 實作 playbook 版本控制（git-based 或 memory store versioning）| version control system |
| 設計 playbook health dashboard（簡單的 markdown report）| health dashboard v0.1 |
| Phase 2 exit criteria check：precision ≥ 0.75？ | go/no-go for Phase 3 |

### Days 25-30: 展望 Phase 3

| 任務 | 預期產出 |
|------|---------|
| 評估 automated Curator 的可行性（哪些 rule 候選需要人工確認？）| Curator automation spec |
| 研究 RLPR fine-tuning 的 timeline 和資源需求 | Phase 3 research plan |
| 設計 regression test suite（讓每次 playbook 更新都自動跑）| regression CI/CD plan |
| 準備 30-day review report（給 manager 的進度報告）| 30-day report |

---

## 附錄 A: 相關概念參考

本架構的設計依據以下已發表的研究和技術分析：

- **ACE Framework** (Stanford/SambaNova, arXiv 2510.04618): Generator/Reflector/Curator 三角色架構；Grow-and-Refine playbook 演化機制
- **MARS** (arXiv 2602.00169): 19-agent 材料科學多智能體系統；16 domain tools 設計參考
- **LLMatDesign** (arXiv 2406.13163): 最接近本方案的 strategy library 機制；ACE 最相容的現有材料科學系統
- **Claude Code Architecture** (Agentic Harness analysis): 三層記憶架構、Permission gating、Plan-Work-Review 循環
- **Tiered Memory**: L1/L2/L3 三層記憶設計，對應本方案的 memory store sharding

---

## 附錄 B: 入職前的自學 Checklist

在正式入職前，建議完成以下技術準備（基於現有 warmup repo 的模組）：

- [ ] 閱讀 ACE paper (arXiv 2510.04618) 全文
- [ ] 實作一個簡單的 evolving playbook demo（不需要 Managed Agents，用 vanilla Claude API 即可）
- [ ] 熟悉 Materials Project API (mp-api) 的基本查詢
- [ ] 閱讀 PyMuPDF 的 table extraction 文件
- [ ] 理解 matminer 的 featurization pipeline
- [ ] 閱讀 wiki/concepts/ace-for-materials.md（本 KB 的核心 mapping 文件）

---

*文件版本: v1.0 | 最後更新: 2026-04-10 | 作者: areomoon*
