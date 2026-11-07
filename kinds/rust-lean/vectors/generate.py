# SPDX-License-Identifier: {{LICENSE_SPDX}}
# SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}
"""Write the golden vectors for {{REPO}} from the reference implementation."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write(name: str, description: str, cases: list[dict], rel: float = 1e-12, abs_: float = 0.0) -> None:
    doc = {"schema": "golden-vectors@1", "description": description, "tolerance": {"rel": rel, "abs": abs_}, "cases": cases}
    (HERE / f"{name}.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    pass  # call write(...) for each group of cases
