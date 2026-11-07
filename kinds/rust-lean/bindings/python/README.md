# {{TITLE}}: Python bindings

Python bindings for [{{REPO}}](https://github.com/{{OWNER}}/{{REPO}}), built from the Rust core with PyO3 and maturin. Function names and results are identical to the Rust crate; the shared golden vectors prove it in CI.

```bash
pip install "git+https://github.com/{{OWNER}}/{{REPO}}@v0.1.0#subdirectory=bindings/python"
```
