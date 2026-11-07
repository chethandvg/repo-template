// SPDX-License-Identifier: {{LICENSE_SPDX}}
// SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}

//! WebAssembly bindings for `{{CRATE}}`. Every function keeps the Rust name, so
//! the golden vectors can call it by name; invalid input throws a JS `Error`.

use wasm_bindgen::prelude::*;

/// The crate version.
#[wasm_bindgen]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_owned()
}
