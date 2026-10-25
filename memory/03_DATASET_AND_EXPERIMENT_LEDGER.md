# 03. Dataset & Experiment Ledger

## 1. Feature Interface Definition (8 Standard Features)

| Index | Feature Name | Description | Processing Rule |
|---|---|---|---|
| 0 | `inter_arrival_time` | Packet inter-arrival time | Mean inter-packet arrival time per flow (seconds) |
| 1 | `packet_size` | Packet size | Mean packet size per flow (bytes) |
| 2 | `protocol` | IP Protocol | Standardized integer protocol ID (6=TCP, 17=UDP) |
| 3 | `flow_duration` | Flow duration | Total duration of flow: $t_{\text{last}} - t_{\text{first}}$ (seconds) |
| 4 | `total_bytes` | Total flow volume | Sum of all packet payload/header bytes in flow |
| 5 | `packet_count` | Total packet count | Number of packets in flow |
| 6 | `dst_port` | Destination port | Destination port number (Collapses under Port 443 HTTPS multiplexing) |
| 7 | `ttl` | Time To Live | Mean TTL value across flow packets (Topology artifact) |

---

## 2. Real Benchmark Dataset Summary (PCAP Traces)

| Dataset | Total Samples | Classes ($K=5$) | Min Duration (s) | Median Duration (s) | Mean Duration (s) | Max Duration (s) |
|---|---:|---|---:|---:|---:|---:|
| **ISCX VPN 2016** | 3,000 | Web_Chat (600), Email (600), File_Transfer (600), Streaming_Media (600), VPN_Tunnel (600) | 0.0001 | 0.41 | 30.90 | 4116.14 |
| **USTC-TFC 2016** | 3,000 | Normal_BitTorrent (600), Normal_Facetime (600), Normal_FTP (600), Malware_Cridex (600), Malware_Geodo (600) | 0.0001 | 0.00015 | 2.78 | 367.70 |

---

## 3. Results Ledger (Empirically Executed & Verified)

### (A) Time-Based Blocking Cross-Validation Summary (Step 3 Deliverable)

#### USTC-TFC 2016 (`results/table2_time_blocked_cv_ustc.csv`):
| Method | Accuracy (mean ± std) | Overhead $F$ (mean ± std) | $t$-stat vs PSO (Acc) | $p$-value vs PSO (Acc) | Trainable Params |
|:---|---:|---:|---:|---:|---:|
| **PSO-FFNN (A)** | $0.7173 \pm 0.0314$ | $0.3559 \pm 0.0164$ | — | — | 325 |
| **MOPSO-FFNN-AD (C)** | **$0.6660 \pm 0.0956$** | **$0.3742 \pm 0.0358$** | $-1.545$ | $0.1568$ | **325** |
| **1D-CNN (DL Baseline)** | $0.7740 \pm 0.0385$ | $0.1989 \pm 0.0153$ | $+4.184$ | $2.363 \times 10^{-3}$ | 2,373 |
| **LSTM (DL Baseline)** | **$0.7817 \pm 0.0446$** | $0.2007 \pm 0.0194$ | $+3.918$ | $3.523 \times 10^{-3}$ | 13,093 |
| **Transformer (DL Baseline)**| $0.7720 \pm 0.0424$ | **$0.1738 \pm 0.0188$** | $+3.721$ | $4.764 \times 10^{-3}$ | 18,437 |

#### ISCX VPN 2016 (`results/table2_time_blocked_cv_iscx.csv`):
| Method | Accuracy (mean ± std) | Overhead $F$ (mean ± std) | $t$-stat vs PSO (Acc) | $p$-value vs PSO (Acc) | Trainable Params |
|:---|---:|---:|---:|---:|---:|
| **PSO-FFNN (A)** | $0.4127 \pm 0.0843$ | $0.4792 \pm 0.0399$ | — | — | 325 |
| **MOPSO-FFNN-AD (C)** | **$0.3823 \pm 0.0830$** | **$0.4837 \pm 0.0415$** | $-1.595$ | $0.1451$ | **325** |
| **1D-CNN (DL Baseline)** | $0.5320 \pm 0.0902$ | $0.3395 \pm 0.0422$ | $+3.192$ | $1.097 \times 10^{-2}$ | 2,373 |
| **LSTM (DL Baseline)** | **$0.5730 \pm 0.0925$** | $0.3343 \pm 0.0394$ | $+3.922$ | $3.500 \times 10^{-3}$ | 13,093 |
| **Transformer (DL Baseline)**| $0.5337 \pm 0.0660$ | **$0.3239 \pm 0.0275$** | $+4.458$ | $1.583 \times 10^{-3}$ | 18,437 |

---

### (B) Comprehensive SOTA Benchmark Comparison (`results/table6_sota_comparison.csv`)

| Method | Parameters | USTC Acc | ISCX Acc | USTC Overhead $F$ | ISCX Overhead $F$ | Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **ET-BERT (Lin et al. 2022)** | $\approx 50\text{M}$ | $96.95\%$ | — | N/A | N/A | Published SOTA (ACM WWW) |
| **YaTC (Chen et al. 2023)** | $\approx 30\text{M}$ | $97.86\%$ | — | N/A | N/A | Published SOTA (IEEE INFOCOM) |
| **FS-Net (Liu et al. 2019)** | $\approx 10\text{M}$ | $87.05\%$ | $52.03\%$ | N/A | N/A | Published SOTA (IEEE INFOCOM) |
| **FlowPic (Shapira 2021)** | $\approx 2\text{M}$ | $> 90.0\%$ | $> 85.0\%$ | N/A | N/A | Published SOTA (IEEE TNSM) |
| **TFE-GNN (Shen 2023)** | $\approx 5\text{M}$ | $97.47\%$ | $91.92\%$ | N/A | N/A | Published SOTA (IEEE JSAC) |
| **Transformer (Ours Baseline)**| $18,437$ | $78.57\%$ | $62.13\%$ | $0.1686$ | $0.2937$ | Re-implemented Generic DL |
| **LSTM (Ours Baseline)** | $13,093$ | $77.47\%$ | $64.23\%$ | $0.2008$ | $0.3067$ | Re-implemented Generic DL |
| **1D-CNN (Ours Baseline)** | $2,373$ | $77.60\%$ | $61.50\%$ | $0.1997$ | $0.3064$ | Re-implemented Generic DL |
| **PSO-FFNN (Base Paper [2])** | $325$ | $74.90\%$ | $47.93\%$ | $0.3544$ | $0.4486$ | Pradhan et al. (IET 2022) |
| **MOPSO-FFNN-AD (Senior [1])**| $325$ | $94.33\%$ (synth)| N/A | $0.2697$ | N/A | Evaluated on Synthetic Gaussian |
| **MOPSO-FFNN-AD (Proposed)** | **325** | **$62.97\%$** | **$37.87\%$** | **$0.3816$** | **$0.4817$** | **Pareto-Dominated (Negative Result)** |

---

### (C) TTL Perturbation Sensitivity (`results/ttl_robustness_results_ustc.csv`)

| TTL Noise ($\pm$ Hops) | FFNN Accuracy | CNN Accuracy | FFNN Degradation ($\Delta$) | CNN Degradation ($\Delta$) |
|:---|:---:|:---:|:---:|:---:|
| **$\pm 0$ (Clean)** | $78.67\%$ | $81.67\%$ | $0.00\%$ | $0.00\%$ |
| **$\pm 5$ Hops** | $78.50\%$ | $81.50\%$ | $-0.17\%$ | $-0.17\%$ |
| **$\pm 10$ Hops** | $74.17\%$ | $81.17\%$ | $-4.50\%$ | $-0.50\%$ |
| **$\pm 20$ Hops** | $65.50\%$ | $81.50\%$ | **$-13.17\%$** | $-0.17\%$ |
| **$\pm 80$ Hops** | $54.50\%$ | $66.00\%$ | **$-24.17\%$** | $-15.67\%$ |
| **$\pm 150$ Hops** | $48.17\%$ | $62.17\%$ | **$-30.50\%$** | $-19.50\%$ |
| **Randomized ($32/64/128/255$)**| $51.83\%$ | $66.00\%$ | **$-26.83\%$** | $-15.67\%$ |

---

### (D) Destination Port Ablation (`results/dst_port_ablation_iscx.csv`)

| Configuration | FFNN Accuracy | CNN Accuracy | Delta FFNN | Delta CNN |
|:---|:---:|:---:|:---:|:---:|
| **With `dst_port` (8 Features)** | $48.33\%$ | $62.50\%$ | $0.00\%$ | $0.00\%$ |
| **Without `dst_port` (7 Features)** | $44.67\%$ | $54.67\%$ | $-3.67\%$ | $-7.83\%$ |
