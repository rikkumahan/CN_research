# 03. Dataset & Experiment Ledger

## 1. Feature Interface Definition (8 Features)

| Index | Feature Name | Description | Processing Rule |
|---|---|---|---|
| 0 | `inter_arrival_time` | Packet inter-arrival time | Mean inter-packet arrival time per flow (seconds) |
| 1 | `packet_size` | Packet size | Mean packet size per flow (bytes) |
| 2 | `protocol` | IP Protocol | Standardized integer protocol ID (6=TCP, 17=UDP) |
| 3 | `flow_duration` | Flow duration | Total duration of flow: $t_{\text{last}} - t_{\text{first}}$ (seconds) |
| 4 | `total_bytes` | Total flow volume | Sum of all packet payload/header bytes in flow |
| 5 | `packet_count` | Total packet count | Number of packets in flow |
| 6 | `dst_port` | Destination port | Destination port number |
| 7 | `ttl` | Time To Live | Mean TTL value across flow packets |

---

## 2. Real Benchmark Dataset Summary (Extracted from Local PCAPs)

| Dataset | Location / Source | Total Samples | Classes ($K=5$) | Min Duration (s) | Median Duration (s) | Mean Duration (s) | Max Duration (s) |
|---|---|---:|---|---:|---:|---:|---:|
| **ISCX VPN 2016** | `c:/dev/raw/ISCX-2016/PCAPs` | 3,000 | Web_Chat (600), Email (600), File_Transfer (600), Streaming_Media (600), VPN_Tunnel (600) | 0.0001 | 18.24 | 26.85 | 114.50 |
| **USTC-TFC 2016** | `c:/dev/raw/USTC-TFC2016` | 3,000 | Normal_BitTorrent (600), Normal_Facetime (600), Normal_FTP (600), Malware_Cridex (600), Malware_Geodo (600) | 0.0001 | 12.50 | 18.40 | 85.20 |

---

## 3. Results Ledger (Empirically Executed & Verified)

### (A) 10-Fold Stratified Cross-Validation Summary — USTC-TFC 2016 (`results/table2_10fold_cv_ustc.csv`)

| Method | Accuracy (mean ± std) | Overhead $F$ (mean ± std) | $t$-statistic vs PSO (Acc) | $p$-value vs PSO (Acc) | $t$-statistic vs PSO ($F$) | $p$-value vs PSO ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (A)** | $0.7490 \pm 0.0230$ | $0.3544 \pm 0.0165$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (C)** | $0.6297 \pm 0.0845$ | $0.3816 \pm 0.0298$ | $-4.071$ | $2.798 \times 10^{-3}$ | $+2.470$ | $3.559 \times 10^{-2}$ | 325 |
| **1D-CNN (DL Baseline)** | $0.7760 \pm 0.0341$ | $0.1997 \pm 0.0152$ | $+2.492$ | $3.431 \times 10^{-2}$ | $-21.493$ | $4.807 \times 10^{-9}$ | 2,373 |
| **LSTM (DL Baseline)** | $0.7747 \pm 0.0348$ | $0.2008 \pm 0.0156$ | $+3.428$ | $7.533 \times 10^{-3}$ | $-35.544$ | $5.462 \times 10^{-11}$ | 13,093 |
| **Transformer (DL Baseline)** | **$0.7857 \pm 0.0407$** | **$0.1686 \pm 0.0130$** | $+2.467$ | $3.577 \times 10^{-2}$ | $-31.320$ | $1.691 \times 10^{-10}$ | 18,437 |

---

### (B) 10-Fold Stratified Cross-Validation Summary — ISCX VPN 2016 (`results/table2_10fold_cv_iscx.csv`)

| Method | Accuracy (mean ± std) | Overhead $F$ (mean ± std) | $t$-statistic vs PSO (Acc) | $p$-value vs PSO (Acc) | $t$-statistic vs PSO ($F$) | $p$-value vs PSO ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (A)** | $0.4793 \pm 0.0288$ | $0.4486 \pm 0.0166$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (C)** | $0.3787 \pm 0.0565$ | $0.4817 \pm 0.0303$ | $-4.025$ | $2.994 \times 10^{-3}$ | $+2.480$ | $3.499 \times 10^{-2}$ | 325 |
| **1D-CNN (DL Baseline)** | $0.6150 \pm 0.0226$ | $0.3064 \pm 0.0094$ | $+14.572$ | $1.450 \times 10^{-7}$ | $-27.729$ | $5.010 \times 10^{-10}$ | 2,373 |
| **LSTM (DL Baseline)** | **$0.6423 \pm 0.0282$** | $0.3067 \pm 0.0110$ | $+18.382$ | $1.908 \times 10^{-8}$ | $-34.575$ | $6.994 \times 10^{-11}$ | 13,093 |
| **Transformer (DL Baseline)** | $0.6213 \pm 0.0308$ | **$0.2937 \pm 0.0207$** | $+8.318$ | $1.618 \times 10^{-5}$ | $-16.613$ | $4.631 \times 10^{-8}$ | 18,437 |

---

### (C) State-of-the-Art Comparison Table (`results/table6_sota_comparison.csv`)

| Method | Accuracy | Composite Overhead $F$ | Parameters | Concept Drift Adapt | Multi-Objective |
|---|---:|---:|---:|---|---|
| **DBN (Shao et al. [7])** | 96.00% (lit) | N/A | N/A | No | No |
| **RNN (Wang et al. [12])** | 94.00% (lit) | N/A | N/A | No | No |
| **1D-CNN (Ours Baseline)** | 77.60% (USTC) / 61.50% (ISCX) | 0.1997 / 0.3064 | 2,373 | No | No |
| **LSTM (Ours Baseline)** | 77.47% (USTC) / 64.23% (ISCX) | 0.2008 / 0.3067 | 13,093 | No | No |
| **Transformer (Ours Baseline)** | **78.57% (USTC)** / 62.13% (ISCX) | **0.1686 / 0.2937** | 18,437 | No | No |
| **PSO-FFNN (Base Paper [2])** | 74.90% (USTC) / 47.93% (ISCX) | 0.3544 / 0.4486 | 325 | No | No |
| **MOPSO-FFNN-AD (Senior [B-Synth])**| 94.33% (Synthetic) | 0.2697 | 325 | Yes (Page-Hinkley) | Yes (6 Sols) |
| **MOPSO-FFNN-AD (Ours [C-Real])**| 62.97% (USTC) / 37.87% (ISCX) | 0.3816 / 0.4817 | 325 | Yes (Page-Hinkley) | Yes (Pareto Front) |
