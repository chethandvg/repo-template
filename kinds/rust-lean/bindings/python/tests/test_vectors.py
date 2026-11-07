# SPDX-License-Identifier: {{LICENSE_SPDX}}
# SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}
"""The shared golden vectors, checked against the Python bindings."""

from pathlib import Path

import {{CRATE_SNAKE}}
from evidence_kernel.vectors import check_dir

VECTORS = Path(__file__).resolve().parents[3] / "vectors"


def test_golden_vectors():
    assert check_dir(VECTORS, {{CRATE_SNAKE}}) > 0
