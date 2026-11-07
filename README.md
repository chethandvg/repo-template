# Repository template for Frequencies of Life

Every [Frequencies of Life](https://chethandvg.github.io/frequencies-of-life/) repository starts from this template, so each one has the same licences, citation metadata, claims ledger, issue forms and CI from its first commit.

## Create a repository

```bash
python scripts/new_repo.py rhythm-units --kind rust-lean --layer 0 --claim-prefix rhythm \
  --title "Rhythm units" --description "Period, frequency and bpm conversions, with proofs." \
  --keywords "rhythm,frequency,lean4,formal-verification,sonification" --out ..
```

The script copies [`common/`](common) and one kind from [`kinds/`](kinds), fills every `{{PLACEHOLDER}}` in file contents and names, adds the licence texts, runs `git init` and sets the local git author. It refuses to overwrite an existing folder and fails if a placeholder is left unfilled.

| Kind | For | Includes |
|---|---|---|
| `rust-lean` | Layer 0 foundations | Rust crate, PyO3 and WebAssembly bindings, Lean 4 proofs with Mathlib, golden vectors |
| `python` | Tools and pure-Python packages | Hatchling package, pytest, Ruff |
| `site` | Static sites | GitHub Pages deployment |

A new `rust-lean` repo fails `cargo test` (and the binding tests) with "no golden-vector cases found" until its first function and golden vector exist. That is deliberate: the shared runner refuses to pass with no cases, so a repo cannot be published untested. Everything else (fmt, clippy, Ruff) passes from the start.

Licences: `--licence apache` (default) or `polyform-nc`, and `--content-licence none`, `cc-by-nc` or `cc-by` for articles, data, figures and audio. The texts in [`licenses/`](licenses) are the official SPDX versions. A content licence also adds `.zenodo.json`, because Zenodo cannot load the two-licence `CITATION.cff`; it records the licence of what the record mainly is (the content licence for `--type dataset`, the code licence for software) and names both in its notes. `--type software` (default) or `dataset` sets `type` in `CITATION.cff` and, when there is one, `upload_type` in `.zenodo.json`.

## What every repository gets

- `README.md` with badges, a generated claims table and a Cite section
- `claims.yaml`, the claims ledger, where each claim states its proof level
- `CITATION.cff`, `AUTHORS`, `AUTHORSHIP.md`, `NOTICE`, `CHANGELOG.md` and `CONTRIBUTING.md`
- Issue forms for bugs and claim corrections, and a pull-request checklist
- CI from [chethandvg/.github](https://github.com/chethandvg/.github): claims, licences, site links, releases, plus the kind's own build and tests

## Licence

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
