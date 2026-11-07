// SPDX-License-Identifier: {{LICENSE_SPDX}}
// SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}

//! Golden-vector tests. The Python and WebAssembly bindings check the same
//! `vectors/*.json` cases, so all three implementations give the same answers.

use golden_vectors::Outcome;
use serde_json::Value;

/// Maps each vector's `fn` name to this crate's implementation.
/// Remove the `allow` once the first function is added.
#[allow(clippy::match_single_binding)]
fn dispatch(name: &str, args: &[Value]) -> Outcome {
    match name {
        // "function_name" => Outcome::from({{CRATE_SNAKE}}::function_name(golden_vectors::f64_arg(args, 0))),
        _ => Outcome::unknown(name, args),
    }
}

#[test]
fn golden_vectors() {
    golden_vectors::check_dir(concat!(env!("CARGO_MANIFEST_DIR"), "/vectors"), dispatch);
}
