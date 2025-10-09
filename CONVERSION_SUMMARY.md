# LaTeX to MyST Markdown Conversion Summary

本文件記錄了從 `workbook/tex/` 到 `wiki/` 的轉換工作。

## 轉換完成時間
2025-10-09

## 目錄結構

已創建以下新目錄結構：

```
wiki/
├── foundations/          # 基礎概念（新建）
├── assumptions/          # 密碼學假設（擴充）
├── primitives/           # 密碼學原語（擴充）
├── advanced/             # 進階主題（新建）
└── exercises/            # 練習題（新建）
```

## 轉換文件清單

### Foundations（基礎）
1. **intro.ipynb** ← `intro.tex` (456 行)
   - 算法定義、可忽略函數、遊戲與漸進安全

2. **notation.ipynb** ← `notation.tex` (59 行)
   - 符號說明

3. **reductions.ipynb** ← `reductions.tex` (246 行)
   - 歸約基礎、碰撞抵抗

### Assumptions（密碼學假設）
4. **discrete-log.ipynb** ← `discrete-log.tex` (部分)
   - 離散對數問題、DDH 假設、OMDL、AOMDL

5. **DDH.ipynb** (已存在，保留)
   - Diffie-Hellman 問題

### Primitives（密碼學原語）
6. **commitments.ipynb** ← `commitments.tex` (268 行)
   - 承諾方案的定義、綁定性、隱藏性

7. **pedersen.ipynb** ← `discrete-log.tex` (部分)
   - Pedersen 承諾、ElGamal 承諾

8. **accumulators.ipynb** ← `accumulators.tex` (320 行)
   - 累加器定義、碰撞自由性

9. **one-time-signatures.ipynb** ← `one-time-sigs.tex` (475 行)
   - 一次性簽名、Lamport 簽名

10. **signatures.ipynb** ← `signatures.tex` (475 行)
    - 數位簽名、Schnorr 簽名、EUF-CMA 安全性

11. **key-tweaking.ipynb** ← `signatures-key-tweaking.tex` (421 行)
    - 密鑰調整、SchnorrSigKP

12. **KE.ipynb** (已存在，保留)
    - 密鑰交換

13. **DHKE.ipynb** (已存在，保留)
    - Diffie-Hellman 密鑰交換

### Advanced Topics（進階主題）
14. **rom.ipynb** ← `rom.tex` (386 行)
    - 隨機預言機模型

15. **fiat-shamir.ipynb** ← `fl.tex` (402 行)
    - Fiat-Shamir 轉換、Forking Lemma

16. **ias.ipynb** ← `ias.tex` (32 行)
    - 互動聚合簽名

### Exercises（練習）
17. **recap-quiz.ipynb** ← `recap-quiz.tex` (235 行)
    - 複習測驗

## 轉換規則

### LaTeX → MyST 語法映射

| LaTeX 環境 | MyST 語法 |
|-----------|----------|
| `\begin{definition}` | `:::{note} Definition` |
| `\begin{theorem}` | `:::{important} Theorem` |
| `\begin{lemma}` | `:::{important} Lemma` |
| `\begin{proof}` | `:::{dropdown} **Proof**` 或 `:::{danger} PROOF :class: dropdown` |
| `\begin{example}` | `:::{tip} Example` |
| `\begin{exercise}` | `:::{exercise}` |
| `\begin{remark}` | `:::{note} Remark` 或 `:::{tip} Remark` |
| `\section{}` | `# Section Title` |
| `\subsection{}` | `## Subsection` |
| `\autoref{}`, `\ref{}` | `[](#label)` |
| `\label{sec:xxx}` | `:label: xxx` |

### 特殊處理

- **數學公式**：保留所有 LaTeX 數學語法（MyST 原生支持）
- **遊戲盒子**：從 cryptocode `tcolorbox` 轉換為簡化的數學塊或代碼塊
- **交叉引用**：添加 `:label:` 標籤，使用 MyST 引用語法
- **解答**：包裹在 `:::{dropdown}` 中實現交互式展開
- **參考文獻**：`\cite{}` 保留或移除（待後續處理）

## myst.yml 更新

已更新 TOC（目錄）結構：
- 添加 Foundations 章節
- 擴展 Assumptions 章節
- 擴展 Primitives 章節
- 添加 Advanced Topics 章節
- 添加 Exercises 章節

## 未轉換文件

以下文件未轉換（不需要或已存在）：
- `abstract.tex` - 摘要（1 行，內容為空）
- `macros.tex` - 宏定義（90 行，供 LaTeX 使用）

## 後續工作建議

1. **測試構建**：運行 `myst build` 檢查是否有語法錯誤
2. **檢查交叉引用**：確認所有內部鏈接正常工作
3. **參考文獻**：如需要，配置 BibTeX 支持
4. **圖片處理**：如有圖片文件，確保路徑正確
5. **樣式調整**：根據需要調整 MyST directive 的樣式選擇

## 文件統計

- 源文件總行數：4277 行（15 個 .tex 文件）
- 轉換後文件數：18 個 .ipynb 文件（包含原有 4 個）
- 新創建文件：14 個
- 新創建目錄：3 個（foundations/, advanced/, exercises/）

## LaTeX 宏處理（已完成）

轉換後的文件包含自定義 LaTeX 宏（來自 `macros.tex`），已使用 `fix_latex_macros.py` 腳本將這些宏展開為標準 LaTeX 命令。

### 宏映射表

| 原宏 | 標準 LaTeX |
|-----|-----------|
| `\algo{...}` | `\mathsf{...}` |
| `\params` | `\mathit{pp}` |
| `\state` | `\mathit{state}` |
| `\sk`, `\pk` | `\mathit{sk}`, `\mathit{pk}` |
| `\adv`, `\bdv` | `\mathcal{A}`, `\mathcal{B}` |
| `\secpar` | `\lambda` |
| `\GG`, `\ZZ`, `\NN` | `\mathbb{G}`, `\mathbb{Z}`, `\mathbb{N}` |
| `\defeq` | `:=` |
| `\sample` | `\leftarrow_R` |
| `\pr{...}` | `\Pr[...]` |
| `\negl` | `\mathrm{negl}` |
| `\advantage{X}{Y}` | `\mathrm{Adv}^{\text{X}}_Y` |
| `\Game` | `\mathsf{Game}` |
| `\grgen` | `\mathsf{GrGen}` |

運行 `python3 fix_latex_macros.py` 即可自動處理所有文件。

## 構建狀態

✅ 已測試構建（`uv run jupyter book start`），所有 18 個文件構建成功，無致命錯誤。
