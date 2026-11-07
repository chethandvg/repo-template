// SPDX-License-Identifier: {{LICENSE_SPDX}}
// SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}

//! Python bindings for `{{CRATE}}`. Every function keeps the Rust name, so the
//! golden vectors can call it by name.

use pyo3::prelude::*;

#[pymodule]
fn {{CRATE_SNAKE}}(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
