# Agentic Service 開發 Warmup 計畫

**目標角色：** 演算法工程師（模型微調 + 算法設計）
**專案背景：** 重點領域 Agent Service，為 Scientists 從 long-context multi-modal source 抽取實驗資料，透過 multi-reasoning 幫助決策協助。
**前提：** 有 ML/NLP 基礎但近期未接觸。
**硬體限制：** Mac（Apple Silicon），本地跑大型模型會卡死，動手任務以雲端 API 為主。

---

## 總覽（6 週計畫）

| 週次 | 主題 | 預估時數 | 週末產出 |
|------|------|----------|----------|
| Week 1 | LLM 基礎回血 | 8–10hr | 能用 API 完成 zero-shot / few-shot / CoT 比較報告 |
| Week 2 | Prompt Engineering → RAG | 10–12hr | 能對一篇論文 PDF 做 RAG 問答的 prototype |
| Week 3 | Agent 架構與框架 | 10–12hr | 用 LangGraph 建出能讀論文 + 抽參數的最小 Agent |
| Week 4 | Multi-modal + Long Context | 8–10hr | 能處理含圖表的論文，輸出結構化數據 |
| Week 5 | 模型微調 + Evaluation | 12–15hr | 完成一次 QLoRA 微調 + eval benchmark |
| Week 6 | 整合演練 + 專案準備 | 12–15hr | 端到端 Scientific Paper Agent demo |

---

## Week 1：LLM 基礎回血

**目標：** 重新建立對現代 LLM 的直覺
**產出：** 一份 prompt 技巧比較報告（zero-shot vs few-shot vs CoT 在科學文本抽取任務的差異）

### 1.1 核心概念快速回顧

| 主題 | 重點 | 推薦資源 |
|------|------|----------|
| Transformer 架構 | Self-attention、KV cache、位置編碼（RoPE, ALiBi） | [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) |
| Decoder-only vs Encoder-Decoder | 為什麼現在主流是 decoder-only | Andrej Karpathy 的 [Let's Build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) |
| Scaling Laws | 模型大小 vs 資料量 vs 計算量的關係 | [Chinchilla paper](https://arxiv.org/abs/2203.15556) 精讀 |
| 量化（Quantization） | GPTQ, AWQ, GGUF, Q4/Q8 的差異與取捨 | [HuggingFace Quantization Guide](https://huggingface.co/docs/transformers/quantization) |

### 1.2 動手任務

> **注意：** 本地跑 Ollama 大型模型會導致 Mac 卡死，所有動手任務改用雲端 API。
> 推薦使用 Gemini API（免費/極低成本）或 OpenAI API。

```python
# 方案 A：用 Gemini API（需申請 API Key + 啟用 billing）
from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

# 方案 B：用 OpenAI API
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
```

嘗試以下 prompt 範例類型（用同一段科學文本測試）：
1. **Zero-shot：** 直接要求抽取實驗參數
2. **Few-shot：** 給 2-3 個範例再要求抽取
3. **Chain-of-thought：** 要求逐步推理後再抽取
4. 比較 `gemini-2.0-flash` vs `gpt-4.1-mini` 在同一任務上的表現

### 1.3 閱讀清單

- [State of GPT — Andrej Karpathy](https://www.youtube.com/watch?v=bZQun8Y4L2A)（1hr，全面概述）
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — 重讀 Transformer 原始論文
- [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223) — 全面 survey

---

## Week 2：Prompt Engineering → RAG

**目標：** 掌握不需訓練就能釋放 LLM 最大化能力的技巧
**產出：** 一個能對科學論文 PDF 做問答並取回實驗參數的 RAG prototype

### 2.1 Prompt Engineering 策略

| 技術 | 說明 | 適用場景 |
|------|------|----------|
| Chain-of-Thought (CoT) | 明確要求逐步推理 | 複雜推理問題 |
| ReAct | Reasoning + Acting 結合 | Agent 設計核心 prompting pattern |
| Self-Consistency | 多次生成取多數 | 需要高可靠性的場景 |
| Tree-of-Thought (ToT) | 探索多條推理路徑 | 需要創造性解法 |
| Structured Output | JSON mode / function calling — 現在主流 API（OpenAI, Gemini, Claude）都原生支援 JSON schema 約束輸出 | 需要程式能解析的結構化輸出 |

### 2.2 RAG（Retrieval-Augmented Generation）

結合檢索與生成 long-context multi-modal source → RAG 是核心基礎

**階段 1：基礎 RAG**
- 文本 loading（PDF, 論文, markdown, txt）
- Chunking 策略（fixed-size, recursive, semantic, sequential）
- Embedding 模型選擇（BGE-M3, GTE-Qwen2, E5-Mistral, Cohere embed-v4）
- Vector DB（FAISS, ChromaDB, Milvus）

**階段 2：進階 RAG**
- Re-ranking（Cohere reranker, cross-encoder）
- Hybrid search（dense + sparse）
- Multi-modal RAG（圖片 + 文字混合檢索）
- Contextual compression
- GraphRAG（知識圖譜增強檢索，適合科學文獻的引用關係）

### 2.3 動手任務

用 LangChain 或 LlamaIndex 建一個簡單 RAG pipeline。

**目標：** 丟入一篇科學論文 PDF，能問答並取回實驗參數

**推薦用 LlamaIndex**（對科學文章比較順暢好用）：

```bash
pip install llama-index llama-index-llms-openai llama-index-embeddings-huggingface
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

# 使用雲端 API 替代本地模型
llm = OpenAI(model="gpt-4.1-mini", temperature=0.1)
documents = SimpleDirectoryReader("./papers").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("What were the experimental conditions?")
```

### 2.4 閱讀清單

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)

---

## Week 3：Agent 架構與框架

**目標：** 理解 Agent 的設計模式與主流框架
**產出：** 用 LangGraph 建出一個能「讀論文 → 抽取實驗參數 → 比較結果」的最小 Agent

### 3.1 Agent 核心概念

**Agent = LLM（大腦）+ Tools（手腳）+ Memory（記憶）+ Planning（規劃）**

**Planning 類型：**
- **ReAct**（最基礎：Reason → Act → Observe loop）
- **Plan-and-Execute**（先規劃再執行）
- **Reflection**（自我檢查 + 修正）
- **LATS**（Language Agent Tree Search）
- **Multi-Agent**（多個 agent 協作）

### 3.2 框架比較

| 框架 | 特點 | 適合場景 | 學習優先度 |
|------|------|----------|-----------|
| LangGraph | 狀態機 + 圖結構，LangChain 生態 | 複雜 multi-step workflow | 高 |
| CrewAI | Multi-agent 協作，角色扮演 | 多 agent 協同任務 | 中 |
| AutoGen | Microsoft 出品，對話式 multi-agent | 研究導向 agent | 中 |
| LlamaIndex Workflows | 資料導向，RAG 整合好 | 知識密集型 agent | 中 |
| Claude Agent SDK | Anthropic 原生，輕量 agent 框架 | 快速建構 Claude-based agent | 中 |
| OpenAI Agents SDK | OpenAI 原生，內建 handoff 機制 | 快速起步，multi-agent 協作 | 中 |

### 3.3 MCP（Model Context Protocol）

MCP 是 2025 年由 Anthropic 提出的開放標準，定義 Agent 與外部工具/資料源的連接協議。

**為什麼重要：**
- 統一了 Agent 呼叫工具的介面（類似 USB-C 之於充電線）
- 主流框架（LangChain, Claude, OpenAI）都已支援或相容
- 你的專案需要連接 PDF parser、Vector DB、計算引擎等多種工具 → MCP 可以標準化這些連接

**核心概念：**
- **MCP Server：** 提供工具/資料的服務端（如 PDF 解析器、資料庫查詢）
- **MCP Client：** Agent 側，負責發現和呼叫 MCP Server
- **Resources / Tools / Prompts：** 三種原語，分別對應資料讀取、動作執行、提示範本

### 3.4 動手任務：用 LangGraph 建一個簡單 Agent

- 建立一個能「讀論文 → 抽取實驗參數 → 比較結果」的 Agent
- 這是你專案用的最小 MVP

**核心組件：**
1. **Tool:** PDF reader + 表格解析
2. **Tool:** 計算/比較引擎
3. **Memory:** 對話歷史 + 已知的資料紀錄
4. **Planner:** ReAct loop

```python
# LangGraph 最小 Agent 骨架
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

@tool
def extract_parameters(text: str) -> dict:
    """Extract experimental parameters from scientific text."""
    # 實作抽取邏輯
    ...

@tool
def compare_results(params_a: dict, params_b: dict) -> str:
    """Compare experimental parameters from two papers."""
    # 實作比較邏輯
    ...

llm = ChatOpenAI(model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools([extract_parameters, compare_results])

graph = StateGraph(AgentState)
# 加入 agent node、tool node、conditional edges...
# 完整實作參考 LangGraph ReAct 教學
```

### 3.5 閱讀清單

- [LLM Powered Autonomous Agents — Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/)（必讀）
- [LangGraph 官方教學](https://langchain-ai.github.io/langgraph/)
- [MCP 官方規格](https://modelcontextprotocol.io/)
- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2404.11584)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

---

## Week 4：Multi-modal + Long Context

**目標：** 掌握處理科學文獻中多模態資訊的技術
**產出：** 能處理含圖表的論文 PDF，輸出結構化 JSON 數據

### 4.1 Multi-modal 模型（2025–2026 現況）

| 模型 | 能力 | 應用 | 備註 |
|------|------|------|------|
| GPT-4.1 / o4-mini | 圖文理解，原生 multi-modal | 通用，性價比高 | API 呼叫 |
| Claude Opus 4 / Sonnet 4 | 圖表、PDF 理解極強 | 科學文獻首選 | API 呼叫 |
| Gemini 2.5 Pro / Flash | 原生 multi-modal，1M context | 超長文獻 | API 呼叫 |
| Qwen3-VL | 開源最強 multi-modal | 可微調 | 需 GPU |
| LLaVA-NeXT | 圖像，可本地部署 | 圖片理解 | 輕量 |
| InternVL2.5 | 圖像，中文好 | 可微調、多語言 | 需 GPU |

### 4.2 科學文獻的 Multi-modal 挑戰

科學論文包含：
- **文字**（摘要、方法、結論）
- **表格**（實驗數據、結果比較）→ 需要 **table extraction**
- **圖片**（實驗照片、光譜圖）→ 需要 **image understanding**
- **圖表**（折線圖、長條圖）→ 需要 **chart understanding**
- **公式** → 需要 **LaTeX / math parsing**
- **引用關係** → 需要 **knowledge graph**

### 4.3 Long Context 技術

你的場景涉及長文獻（科學論文 ~10-50 頁），需要了解：

| 技術 | 說明 | 適用場景 |
|------|------|----------|
| 長上下文模型 | Gemini 2.5 Pro 1M tokens, Claude 200K | 整篇丟入 |
| RAG | 切 chunk → 檢索 → 生成 | 成本考量或需精確定位段落 |
| Map-Reduce | 分段處理 → 合併結果 | 可處理任意長度 |
| Hierarchical Summarization | 多層摘要 | 超長文獻 |
| Sliding Window + Attention Sink | 串流處理超長文本通道 | 避免關鍵資訊流失 |

### 4.4 動手任務

```python
# 用雲端 API 測試 multi-modal 能力（不需本地 GPU）
# 方案 A：OpenAI
from openai import OpenAI
import base64

client = OpenAI()

with open("experiment_chart.png", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "請分析這張實驗圖表，提取所有數據趨勢並以 JSON 格式輸出"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
        ]
    }],
    response_format={"type": "json_object"},  # 原生 JSON mode
)
print(response.choices[0].message.content)

# 方案 B：Gemini（支援更長 context）
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client(api_key="YOUR_KEY")
image = types.Part.from_bytes(
    data=Path("experiment_chart.png").read_bytes(),
    mime_type="image/png",
)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["請分析這張實驗圖表，提取所有數據趨勢", image],
)
print(response.text)
```

### 4.5 閱讀清單

- [A Survey on Multimodal Large Language Models](https://arxiv.org/abs/2306.13549)
- [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449) — 直接用視覺模型做文件檢索
- [DocLLM: A Layout-aware LLM for Document Understanding](https://arxiv.org/abs/2401.00908)

---

## Week 5：模型微調 + Evaluation

**目標：** 掌握 LLM 微調的完整流程，以及如何建立 evaluation benchmark
**產出：** 完成一次 QLoRA 微調實驗 + eval benchmark 比較報告

### 5.1 微調方法概覽

| 方法（由輕到重） | 說明 |
|-----------------|------|
| Prompt Tuning | 只調 prompt embeddings（最輕） |
| LoRA / QLoRA | 低秩適配，額外少量參數（主流） |
| Adapter Tuning | 插入 adapter 層 |
| Full Fine-tuning | 全參數微調（需要大量 GPU） |
| Continued Pre-training | 用領域資料繼續預訓練（最重） |

### 5.2 你的專案應用可能的微調場景

| 場景 | 方法 | 資料需求 |
|------|------|----------|
| 讓模型更理解特定學術領域 | Continued Pre-training + LoRA | 領域文獻 corpus |
| 精準抽取特定格式的實驗數據 | SFT (Supervised Fine-Tuning) + LoRA | 標記好的 (input, output) pairs |
| 讓模型判斷結果是否合理 | RLHF / DPO | 人類標注的偏好對照 |
| 讓模型更好地理解特殊圖表 | Multi-modal SFT | 圖表 + 描述 pairs |

### 5.3 Evaluation（評估方法）

> **Evaluation 比 Training 更重要** — 沒有好的 eval，你無法知道微調是否真的有效。

#### 5.3.1 建立 Benchmark 資料集

```python
# 手動標註 50-100 筆「論文段落 → 結構化參數」的 ground truth
eval_data = [
    {
        "input": "The reaction was carried out at 37°C in PBS buffer (pH 7.2) for 24 hours...",
        "expected": {
            "temperature": "37°C",
            "buffer": "PBS",
            "pH": 7.2,
            "duration": "24 hours"
        }
    },
    # ... 更多標註資料
]
```

#### 5.3.2 Evaluation Metrics

| 指標 | 說明 | 適用場景 |
|------|------|----------|
| **Exact Match (EM)** | 抽取結果是否完全一致 | 結構化欄位（溫度、pH） |
| **F1 Score** | 部分匹配的精確率/召回率 | 文字描述類欄位 |
| **LLM-as-Judge** | 用另一個強模型（如 Claude Opus）評分 | 開放式回答、推理品質 |
| **Human Eval** | 領域專家人工評估 | 最終驗收，最可靠 |

#### 5.3.3 A/B 比較框架

```python
import json

def evaluate_extraction(model_fn, eval_data: list[dict]) -> dict:
    """對一個模型函式跑完整 eval，回傳 metrics。"""
    exact_matches = 0
    total_fields = 0
    matched_fields = 0

    for sample in eval_data:
        prediction = model_fn(sample["input"])
        expected = sample["expected"]

        for key, value in expected.items():
            total_fields += 1
            pred_value = prediction.get(key)
            if pred_value == value:
                exact_matches += 1
                matched_fields += 1
            elif pred_value is not None:
                # 部分匹配邏輯（如字串相似度）
                matched_fields += 0.5

    return {
        "exact_match_rate": exact_matches / total_fields,
        "f1_score": matched_fields / total_fields,
        "total_samples": len(eval_data),
    }

# 比較：基礎模型 vs 微調模型 vs prompt engineering
results_base = evaluate_extraction(base_model_extract, eval_data)
results_finetuned = evaluate_extraction(finetuned_extract, eval_data)
results_prompted = evaluate_extraction(prompted_extract, eval_data)
print(json.dumps({"base": results_base, "finetuned": results_finetuned, "prompted": results_prompted}, indent=2))
```

### 5.4 QLoRA 微調實戰

> **Apple Silicon 注意事項：**
> `bitsandbytes` 的 4-bit 量化對 MPS (Apple Silicon) 支援有限。建議方案：
> - **方案 A（推薦）：** 使用 Google Colab (T4 GPU 免費) 或 Kaggle Notebooks (P100 免費)
> - **方案 B：** 用 `mlx-lm`（Apple 的 MLX 框架），原生支援 Apple Silicon 微調
> - **方案 C：** 租用雲端 GPU（Lambda Labs, RunPod, Vast.ai）

**環境準備（Colab / Linux GPU）：**

```bash
pip install transformers peft trl datasets bitsandbytes accelerate
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from datasets import Dataset

# 1. 載入模型 (4-bit 量化)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)

model_name = "Qwen/Qwen2.5-7B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# 2. 設定 LoRA
lora_config = LoraConfig(
    r=16,              # LoRA rank
    lora_alpha=32,     # scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → trainable params: ~4M / total: ~7B (0.06%)

# 3. 準備訓練資料（你的領域科學資料格式）
train_data = Dataset.from_list([
    {
        "text": """<|im_start|>system
You are a scientific data extraction assistant.<|im_end|>
<|im_start|>user
Extract experimental parameters from:
"We conducted the experiment at 25°C with pH 7.4 buffer..."<|im_end|>
<|im_start|>assistant
{
    "temperature": "25°C",
    "pH": 7.4,
    "medium": "buffer"
}<|im_end|>"""
    },
    # ... 更多標註資料（建議至少 200-500 筆）
])

# 4. 設定訓練參數並啟動
training_config = SFTConfig(
    output_dir="./lora-science-extractor",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    fp16=True,
    optim="paged_adamw_8bit",
    warmup_ratio=0.05,
    max_seq_length=2048,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_data,
    args=training_config,
)

trainer.train()
trainer.save_model("./lora-science-extractor")
```

**Apple Silicon 替代方案（MLX）：**

```bash
pip install mlx-lm
```

```bash
# 直接用 MLX 做 LoRA 微調（原生支援 Apple Silicon）
mlx_lm.lora \
    --model Qwen/Qwen2.5-7B-Instruct \
    --data ./train_data \
    --train \
    --num-layers 8 \
    --batch-size 2 \
    --iters 500
```

### 5.5 微調後部署

```bash
# 合併 LoRA adapter → 導出 GGUF → 匯入 Ollama

# 1. 合併 adapter
python -c "
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct')
model = PeftModel.from_pretrained(base, './lora-science-extractor')
model = model.merge_and_unload()
model.save_pretrained('./merged-model')
"

# 2. 轉 GGUF（用 llama.cpp）
python convert_hf_to_gguf.py ./merged-model --outfile model.gguf --outtype q4_K_M

# 3. 建立 Ollama Modelfile
cat > Modelfile <<EOF
FROM ./model.gguf
SYSTEM "You are a scientific data extraction assistant specialized in extracting experimental parameters from research papers."
PARAMETER temperature 0.1
EOF

# 4. 匯入 Ollama
ollama create science-extractor -f Modelfile
ollama run science-extractor
```

> **注意：** 部署到 Ollama 跑推理（inference）的資源需求遠低於訓練。
> 7B 模型 Q4 量化後僅需 ~5GB RAM，Mac 日常推理不會卡死。
> 卡死問題主要發生在同時跑多個大模型或做本地訓練時。

### 5.6 閱讀清單

- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
- [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290)
- [HuggingFace PEFT 官方教學](https://huggingface.co/docs/peft)
- [MLX Fine-tuning Guide](https://github.com/ml-explore/mlx-examples/tree/main/llms/mlx_lm)

---

## Week 6：整合演練 + 專案準備

**目標：** 把前 5 週學到的串起來，做一個 end-to-end demo
**產出：** 可展示的 Scientific Paper Agent demo + eval 結果報告

### 6.1 Mini Project：Scientific Paper Agent

**架構：**

```
┌─────────────────────────────────┐
│      Orchestrator Agent         │
│    (LangGraph / CrewAI)         │
├─────────┬──────────┬────────────┤
│ Extractor│ Analyzer │  Advisor   │
│  Agent   │  Agent   │  Agent     │
├─────────┼──────────┼────────────┤
│PDF/Image│ Compare  │ Reasoning  │
│ Parser  │ Engine   │  Engine    │
│(multi-  │ (table   │ (CoT/ToT)  │
│ modal)  │  diff)   │            │
├─────────┴──────────┴────────────┤
│      Shared Memory / RAG        │
│ (Vector DB + Extracted Data     │
│             Store)              │
└─────────────────────────────────┘
```

**工具連接（可用 MCP 標準化）：**
- PDF Parser → MCP Server
- Vector DB → MCP Server
- Compare Engine → MCP Server

### 6.2 驗收標準

- [ ] 能匯入一篇科學論文 PDF（含圖表）
- [ ] 能自動抽取：實驗條件、數據結果、結論摘要
- [ ] 能跨多篇論文比較相同實驗條件
- [ ] 能用 CoT/ToT 解釋推理過程
- [ ] 用微調模型 vs 基礎模型 vs prompt engineering 做 A/B 比較
- [ ] 有量化的 eval 結果（EM / F1 / LLM-as-Judge 分數）

### 6.3 專案準備 Checklist

- [ ] 確認團隊使用的 LLM provider（雲端 API or 自部署）
- [ ] 確認科學領域的資料來源與格式
- [ ] 確認 evaluation metrics（準確率、召回率、人類評估）
- [ ] 準備模型監控的 pipeline 與工具
- [ ] 確認 GPU 資源（雲端用 A100/H100 or Apple Silicon）
- [ ] 了解團隊是否採用 MCP 或其他 tool protocol

---

## 日常學習資源

### 必追

| 資源 | 類型 | 用途 |
|------|------|------|
| [Lilian Weng's Blog](https://lilianweng.github.io/) | Blog | OpenAI 研究員，Agent/LLM 文章品質極高 |
| [The Batch (Andrew Ng)](https://www.deeplearning.ai/the-batch/) | Newsletter | AI 趨勢 |
| [Latent Space Podcast](https://www.latent.space/) | Podcast | AI 工程深度訪談 |
| [HuggingFace Blog](https://huggingface.co/blog) | Blog | 開源模型最新動態 |
| [ArXiv daily (Papers With Code)](https://paperswithcode.com/) | 論文 | 追蹤最新研究 |

### 實戰課程

| 課程 | 類型 | 時間 | 學習優先度 |
|------|------|------|-----------|
| [DeepLearning.AI: LangChain/LangGraph](https://www.deeplearning.ai/) | Agent 框架實戰 | 各 1–2hr | 高 |
| [DeepLearning.AI: Fine-tuning LLMs](https://www.deeplearning.ai/) | 微調入門 | 1hr | 高 |
| [HuggingFace NLP Course](https://huggingface.co/learn/nlp-course) | Transformer 到模型微調全過程 | 自訂 | 中 |
| [Full Stack LLM Bootcamp](https://fullstackdeeplearning.com/) | 從零到部署 | ~10hr | 中 |

---

## 重點提醒

1. **不要從頭訓練模型** — 2024–2026 的主流是在現有的 base model 上做 LoRA 微調或 prompt engineering
2. **先跑通 pipeline 再美化** — 先用 API（GPT-4.1/Claude/Gemini）驗證可行性，再考慮自部署/微調
3. **Evaluation 比 Training 更重要** — 沒有量化指標就不要微調，先建好 benchmark 再動手
4. **Multi-modal 是核心趨勢** — 做出能處理表格與圖片的 agent 比純文字 agent 更有競爭力
5. **跟團隊對齊技術棧** — 先瞭解團隊用什麼框架再深入學習，避免學了用不上
6. **善用免費雲端資源** — Google Colab (T4)、Kaggle (P100) 足以完成 7B 模型的 QLoRA 微調，不需要買 GPU
