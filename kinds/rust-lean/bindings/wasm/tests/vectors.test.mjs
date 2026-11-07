// SPDX-License-Identifier: {{LICENSE_SPDX}}
// SPDX-FileCopyrightText: {{YEAR}} {{AUTHOR}}
// The shared golden vectors, checked against the WebAssembly build.

import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { test } from "node:test";
import { checkDir } from "golden-vectors";

const impl = createRequire(import.meta.url)("../pkg/node/{{CRATE_SNAKE}}_wasm.js");

test("golden vectors", () => {
  assert.ok(checkDir(new URL("../../../vectors/", import.meta.url), impl) > 0);
});
