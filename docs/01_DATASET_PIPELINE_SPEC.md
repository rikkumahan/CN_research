# Review 2 — Dataset & Preprocessing Specification

## Goal

Replace the synthetic dataset in the senior implementation with real public traffic datasets while preserving the eight-feature input interface used by the FFNN.

## Datasets

1. ISCX VPN/non-VPN 2016
2. USTC-TFC 2016

## Required feature schema

Every processed flow must expose:

| Column | Meaning |
|---|---|
| `inter_arrival_time` | Flow/packet inter-arrival statistic used consistently across datasets |
| `packet_size` | Packet-size statistic used consistently |
| `protocol` | Protocol representation |
| `flow_duration` | Flow duration |
| `total_bytes` | Total bytes in the flow |
| `packet_count` | Number of packets |
| `dst_port` | Destination port |
| `ttl` | TTL statistic |

Plus:
- `label`
- `dataset`
- optional `flow_id` / provenance fields

## Critical methodological requirement

Define the feature-extraction rule precisely and use the same semantic definition on both datasets.

Examples that must be explicitly decided and documented:
- whether packet-size is first/mean/max/other statistic
- whether inter-arrival time is mean/median/other statistic
- how bidirectional flows are grouped
- how missing TTL values are handled
- how non-TCP/UDP protocols are represented
- how destination port is selected for a bidirectional flow
- how duplicate flows are removed

Do not silently make incompatible definitions between datasets.

## Label mapping

Create an explicit mapping file:

```text
dataset -> raw label -> normalized label
```

Never infer class names from a screenshot or from accuracy numbers.

Save:

```text
data/metadata/label_mapping.json
data/metadata/dataset_statistics.json
```

## Preprocessing sequence

Recommended pipeline:

```text
PCAP / original flow files
        ↓
flow construction / parsing
        ↓
8-feature extraction
        ↓
label assignment
        ↓
quality checks
        ↓
duplicate / invalid-flow handling
        ↓
saved processed CSV/Parquet
        ↓
train/validation/test or CV split
        ↓
training-only normalization
```

## Quality checks

Automatically report:

- number of rows
- number of classes
- class distribution
- missing values per feature
- infinite values
- duplicate count
- min/median/mean/max for numeric features
- protocol/value distribution
- destination-port distribution
- flow-duration distribution

## Leakage prevention

For CV:
- split first
- fit scaler on training portion only
- transform validation/test using training scaler only

If flows from the same capture/session can produce highly correlated samples, inspect whether random row-level splitting would leak session information. If grouping by capture/session is necessary and feasible, document it.

## Output schema

Preferred:

```text
data/
├── raw/                 # not committed if large
├── processed/
│   ├── iscx_flows.csv
│   └── ustc_flows.csv
└── metadata/
    ├── label_mapping.json
    └── dataset_statistics.json
```

## Deliverable table

Generate a machine-readable CSV and paper-ready table:

| Dataset | Classes | Samples | Min Duration | Median Duration | Mean Duration | Max Duration |
|---|---:|---:|---:|---:|---:|---:|

Also generate class counts:

| Dataset | Class | Samples |
|---|---|---:|

## Important

Do not claim "PCAP → exact eight features" unless the resulting pipeline actually performed that conversion or an equivalent raw-flow extraction with documented provenance.

