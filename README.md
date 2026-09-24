---
pretty_name: Open-UTS (126 Univariate Time Series)
language:
- zxx
license: other
tags:
- time-series
- anomaly-detection
- tsb-ad
---

# Open-UTS: 126 Univariate Time Series

Open-UTS contains **126 complete univariate time series from nine original datasets**. All 126 are from the Eval 350 collection of the pinned, private [TSB-AD-U baseline](https://huggingface.co/datasets/MathewShen/tsb-ad-u), revision `c6aded12d5657b96d83595500eb60c1412c8c3a2`. It is an unofficial redistribution of selected [TSB-AD](https://github.com/TheDatumOrg/TSB-AD) series, not a new blind benchmark. The other 696 series from the 822-series baseline are not in this release.

The data have **mixed licenses**, not a single license granted by this repository. Read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) before reuse; the original source licenses and attribution requirements still apply. The selection excludes GPL, noncommercial, permission-dependent, and insufficiently documented sources from this particular release.

## Data and labels

`data/test.parquet` contains one complete sequence per row, with 10,691,121 observations in total. The Hub split is named `test` for benchmark evaluation; each row also includes its training prefix.

| Column | Type | Meaning |
| --- | --- | --- |
| `id` | string | Pinned TSB-AD-U series ID |
| `source` | string | Original dataset name; reporting metadata only |
| `values` | list<float64> | Complete observations in original sampling order |
| `labels` | list<bool> | Unchanged labels from the pinned baseline |
| `train_end` | int64 | Exclusive end of the training prefix |
| `original_sha256` | string | SHA-256 of the retained TSB-AD source CSV |
| `labels_corrected` | list<bool or null> | Original labels with demonstrably unlabeled positions restored to null |

In the public subset, 22 NAB series have an unlabeled initialization region in the training prefix, and the Daphnet series has positions outside the annotated experiment. Those positions are `null` in `labels_corrected`, not negative examples. This accounts for 21,633 unknown training points and 12,440 unknown evaluation points. The exact zero-based, half-open intervals and reasons are in [CORRECTIONS.json](CORRECTIONS.json); the relevant original-file and offset evidence is in [source-mappings.json](source-mappings.json). Other labels remain unchanged; unchanged does **not** imply every point was independently verified. The original `labels` column is untouched.

No `labels_annotated` column is released here. The current model-assisted annotation candidates lack human review and should not be presented as supervised ground truth. An evaluation using `labels_corrected` needs a specified null-aware metric protocol: filling null with zero or deleting it and joining the timeline would change the task.

The observations, original labels, row IDs, train boundaries, and CSV hashes were checked against the pinned baseline before export. [MANIFEST.json](MANIFEST.json) records the exported file checksum and CATSv2 source alignment. Run `uv run --with pyarrow python verify.py` to check the distributed file, schema, row counts, sources, and nullable-label invariants.

Example usage after publication:

```python
from datasets import load_dataset

rows = load_dataset("MathewShen/open-uts", split="test", revision="PINNED_COMMIT")
row = rows[0]
train_values = row["values"][:row["train_end"]]
test_values = row["values"][row["train_end"]:]
test_labels = row["labels_corrected"][row["train_end"]:]
```

The source name and ID must not drive anomaly-detector candidate generation, routing, or hyperparameters. Keep evaluation labels out of model fitting and selection. All 126 sequences have been exposed to development work; this is not an untouched test set.

## Source distribution

| Source | Series | License |
| --- | ---: | --- |
| CATSv2 | 1 | CC BY 4.0 |
| Daphnet | 1 | CC BY 4.0 |
| LTDB | 8 | ODC-By 1.0 |
| MGAB | 8 | CC0 1.0 |
| MITDB | 7 | ODC-By 1.0 |
| NAB | 23 | MIT |
| OPPORTUNITY | 27 | CC BY 4.0 |
| SMD | 33 | MIT |
| SVDB | 18 | ODC-By 1.0 |

The original values and labels of the CATSv2 row were independently matched to `bso2[4,300,000:4,600,000]` and `y[4,300,000:4,600,000]` in [Zenodo 8338435](https://doi.org/10.5281/zenodo.8338435). The maximal observation difference is `7.11e-15`; all 300,000 original labels match the source's `y` column. See [MANIFEST.json](MANIFEST.json) for the source-file checksum.

## Status and provenance

The original and corrected labels come from a broader, still ongoing source audit. The corrections in this subset are limited to NAB and Daphnet. This subset does not certify the excluded sources or finish the requested human annotations.
