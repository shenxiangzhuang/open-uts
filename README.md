---
pretty_name: Open-UTS
language:
- zxx
license: other
tags:
- time-series
- anomaly-detection
---

# Open-UTS

Open-UTS contains **126 univariate time series** from nine datasets for anomaly detection. Each row in `data/test.parquet` is one complete sequence, including its training segment.

| Column | Description |
| --- | --- |
| `values` | Observations in time order |
| `labels` | Original anomaly labels, unchanged |
| `labels_corrected` | Labels with known unlabeled positions set to `null` |
| `train_end` | First index after the training segment |
| `id`, `source`, `original_sha256` | Series ID, source dataset, and source-file checksum |

`null` means **unknown**, not normal. The corrected intervals are listed in [CORRECTIONS.json](CORRECTIONS.json).

```python
from datasets import load_dataset

row = load_dataset("MathewShen/open-uts", split="test")[0]
train = row["values"][:row["train_end"]]
test = row["values"][row["train_end"]:]
test_labels = row["labels_corrected"][row["train_end"]:]
```

The nine sources have different licenses. See [source credits and license terms](THIRD_PARTY_NOTICES.md) before reuse. File checksums and source counts are in [MANIFEST.json](MANIFEST.json).
