"""Check the public package's content and integrity: uv run --with pyarrow python verify.py."""

import hashlib
import json
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    assert manifest["rows"] == 126
    assert manifest["columns"] == [
        "id",
        "source",
        "values",
        "labels",
        "train_end",
        "original_sha256",
        "labels_corrected",
    ]
    corrections = json.loads((root / "CORRECTIONS.json").read_text())
    changes = {row["id"]: row for row in corrections["changes"]}
    assert len(changes) == 23
    mappings = json.loads((root / "source-mappings.json").read_text())
    assert len(mappings) == 24 and set(changes) <= {row["id"] for row in mappings}
    counts, seen = Counter(), set()
    for name, info in manifest["files"].items():
        path = root / name
        with path.open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == info["sha256"]
        table = pq.read_table(path)
        assert table.column_names == manifest["columns"]
        assert table.num_rows == info["rows"]
        points = train_unknown = test_unknown = 0
        for row in table.to_pylist():
            ident = row["id"]
            assert ident not in seen
            seen.add(ident)
            counts[row["source"]] += 1
            values, labels, corrected = (
                row["values"],
                row["labels"],
                row["labels_corrected"],
            )
            end = row["train_end"]
            assert 0 < end < len(values) == len(labels) == len(corrected)
            expected = labels.copy()
            if ident in changes:
                assert changes[ident]["source"] == row["source"]
                for start, stop in changes[ident]["ranges"]:
                    assert 0 <= start < stop <= len(labels)
                    expected[start:stop] = [None] * (stop - start)
            assert corrected == expected
            points += len(values)
            train_unknown += sum(y is None for y in corrected[:end])
            test_unknown += sum(y is None for y in corrected[end:])
        assert (points, train_unknown, test_unknown) == (
            info["points"],
            info["train_unknown"],
            info["test_unknown"],
        )
    assert len(seen) == 126 and set(changes) <= seen
    assert dict(sorted(counts.items())) == manifest["sources"]
    print(f"Verified {len(seen)} series from {len(counts)} sources")


if __name__ == "__main__":
    main()
