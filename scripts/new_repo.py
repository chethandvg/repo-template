# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Chethan Dandebala Venkatarama
"""Create a new Frequencies of Life repository from this template.

    python scripts/new_repo.py rhythm-units --kind rust-lean --layer 0 --claim-prefix rhythm \
        --title "Rhythm units" --description "Period, frequency and bpm conversions ..." \
        --keywords "rhythm,frequency,lean4,formal-verification,sonification" --out E:/Projects/beginning-of-life

It copies common/ and kinds/<kind>/ into <out>/<name>, fills every {{PLACEHOLDER}}
(file contents and file names), adds the licence files, runs `git init`, and sets
the local git author name. It refuses to overwrite an existing folder and fails
if any placeholder is left unfilled.

With a content licence, CITATION.cff lists two licences, which Zenodo's CITATION.cff
importer cannot load (it reads `license` as one string). So the script also writes
.zenodo.json, which Zenodo reads instead, from the same values.
"""

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
LICENCES = {"apache": "Apache-2.0", "polyform-nc": "PolyForm-Noncommercial-1.0.0"}
CONTENT = {"none": None, "cc-by-nc": "CC-BY-NC-4.0", "cc-by": "CC-BY-4.0"}
NAMES = {
    "Apache-2.0": "Apache-2.0",
    "PolyForm-Noncommercial-1.0.0": "the PolyForm Noncommercial License 1.0.0",
    "CC-BY-NC-4.0": "CC BY-NC 4.0",
    "CC-BY-4.0": "CC BY 4.0",
}
ZENODO_LICENCES = {  # SPDX id -> Zenodo licence id
    "Apache-2.0": "apache-2.0",
    "PolyForm-Noncommercial-1.0.0": "polyform-noncommercial-1.0.0",
    "CC-BY-NC-4.0": "cc-by-nc-4.0",
    "CC-BY-4.0": "cc-by-4.0",
}
CONTENT_SCOPE = "articles, data, figures and audio"
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def zenodo_json(v: dict[str, str], keywords: list[str]) -> str:
    """.zenodo.json from the CITATION.cff values. Zenodo records one licence, so the record shows the
    licence of what it mainly is (the content licence for a dataset, the code licence for software),
    with a note naming both."""
    code, content = v["LICENSE_SPDX"], v["CONTENT_SPDX"]
    shown, which = (content, "content") if v["CFF_TYPE"] == "dataset" else (code, "code")
    if shown not in ZENODO_LICENCES:
        sys.exit(f"no Zenodo licence id for {shown}; add it to ZENODO_LICENCES in scripts/new_repo.py")
    out = {
        "upload_type": v["CFF_TYPE"],
        "title": v["TITLE"],
        "description": v["DESCRIPTION"],
        "creators": [
            {
                "name": f"{v['AUTHOR_FAMILY']}, {v['AUTHOR_GIVEN']}",
                "orcid": v["ORCID"].removeprefix("https://orcid.org/"),
            }
        ],
        "license": ZENODO_LICENCES[shown],
        "keywords": keywords,
        "notes": (
            f"Dual licence: the {CONTENT_SCOPE} are under {NAMES[content]} (LICENSES/{content}.txt); "
            f"the code is under {NAMES[code]} (LICENSE). "
            f"Zenodo records one licence, so this {v['CFF_TYPE']} record shows the {which} licence."
        ),
    }
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def licence_section(code: str, content: str | None) -> str:
    if code == "Apache-2.0":
        text = "Code: Apache-2.0 ([LICENSE](LICENSE))."
    else:
        text = (
            "Code: free for non-commercial use under the PolyForm Noncommercial License 1.0.0 "
            "([LICENSE](LICENSE)). For commercial use, see [COMMERCIAL.md](COMMERCIAL.md)."
        )
    if content:
        text += f" {CONTENT_SCOPE.capitalize()}: {NAMES[content]} ([LICENSES/{content}.txt](LICENSES/{content}.txt))."
    return text + " Copyright notices are in [NOTICE](NOTICE)."


def values(a: argparse.Namespace, site: dict) -> dict[str, str]:
    code, content = LICENCES[a.licence], CONTENT[a.content_licence]
    keywords = [k.strip() for k in a.keywords.split(",") if k.strip()]
    cff_keywords = keywords or ["frequencies-of-life"]
    snake = a.name.replace("-", "_").replace(".", "_")
    given, _, family = site["author"].partition(" ")
    kind = json.loads((HERE / "kinds" / a.kind / "kind.json").read_text(encoding="utf-8"))
    today = datetime.date.today()
    v = {
        "REPO": a.name,
        "CFF_TYPE": a.type,
        "TITLE": a.title,
        "DESCRIPTION": a.description,
        # Quoted and escaped once, for quoted fields in YAML, TOML and JSON (JSON escapes are valid in all three).
        "TITLE_Q": json.dumps(a.title, ensure_ascii=False),
        "DESCRIPTION_Q": json.dumps(a.description, ensure_ascii=False),
        "CRATE": a.name,
        "CRATE_SNAKE": snake,
        "PY_MODULE": snake,
        "LEAN_LIB": "".join(part.capitalize() for part in re.split(r"[-_.]", a.name)),
        "LEAN_PKG": snake,
        "CLAIM_PREFIX": a.claim_prefix,
        "LAYER": a.layer,
        "LICENSE_SPDX": code,
        "CONTENT_SPDX": content or "",
        "LICENSE_BADGE": code.replace("-", "--"),
        "LICENSE_CFF": f" {code}" if not content else f"\n  - {code}\n  - {content}",
        "LICENCE_SECTION": licence_section(code, content),
        "REQUIRED_NOTICE": (
            f"\nRequired Notice: Copyright {today.year} {site['author']} (https://github.com/{site['owner']})\n"
            if code.startswith("PolyForm")
            else ""
        ),
        "YEAR": str(today.year),
        "DATE": today.isoformat(),
        "OWNER": site["owner"],
        "AUTHOR": site["author"],
        "AUTHOR_GIVEN": given,
        "AUTHOR_FAMILY": family,
        "ORCID": site["orcid"],
        "SITE_URL": site["site_url"],
        "PROJECT_URL": site["site_url"] + site["project_path"],
        "SERIES": site["series"],
        "KEYWORDS_YAML": "\n".join(f"  - {k}" for k in cff_keywords),
        "KEYWORDS_TOML": json.dumps(keywords[:5]),
        "KEYWORDS_JSON": json.dumps(keywords),
        "ZENODO_STANDARD": (
            "\n- Zenodo reads `.zenodo.json` instead of `CITATION.cff`, so keep the two in step." if content else ""
        ),
    }
    v["ZENODO_JSON"] = zenodo_json(v, cff_keywords) if content else ""
    v["USAGE"] = PLACEHOLDER.sub(lambda m: v[m.group(1)], kind["usage"])
    v["VERIFIED"] = PLACEHOLDER.sub(lambda m: v[m.group(1)], kind["verified"])
    v["EXTRA_BADGES"] = PLACEHOLDER.sub(lambda m: v[m.group(1)], kind.get("badges", ""))
    return v


def render(src_root: Path, dest: Path, v: dict[str, str]) -> None:
    for src in sorted(src_root.rglob("*")):
        rel = src.relative_to(src_root)
        if src.is_dir() or rel.name == "kind.json":
            continue
        target = dest / PLACEHOLDER.sub(lambda m: v[m.group(1)], rel.as_posix())
        target.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        target.write_text(PLACEHOLDER.sub(lambda m: v[m.group(1)], text), encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="repository name, kebab-case")
    ap.add_argument("--kind", required=True, choices=sorted(p.name for p in (HERE / "kinds").iterdir()))
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", required=True)
    ap.add_argument("--layer", required=True, choices=["meta", "0", "1", "2", "3"])
    ap.add_argument("--claim-prefix", required=True)
    ap.add_argument("--licence", choices=LICENCES, default="apache")
    ap.add_argument("--content-licence", choices=CONTENT, default="none")
    ap.add_argument(
        "--type",
        choices=["software", "dataset"],
        default="software",
        help="type in CITATION.cff and upload_type in .zenodo.json (default: software)",
    )
    ap.add_argument("--keywords", default="", help="comma-separated; the first five also go to crates.io")
    ap.add_argument("--out", type=Path, required=True, help="parent folder for the new repo")
    ap.add_argument("--site-json", type=Path, default=HERE.parent / ".github" / "site.json")
    a = ap.parse_args()

    dest = a.out / a.name
    if dest.exists():
        sys.exit(f"{dest} already exists; refusing to overwrite it")
    site = json.loads(a.site_json.read_text(encoding="utf-8"))
    v = values(a, site)

    render(HERE / "common", dest, v)
    render(HERE / "kinds" / a.kind, dest, v)
    shutil.copyfile(HERE / "licenses" / f"{v['LICENSE_SPDX']}.txt", dest / "LICENSE")
    if content := v["CONTENT_SPDX"]:
        (dest / "LICENSES").mkdir(exist_ok=True)
        shutil.copyfile(HERE / "licenses" / f"{content}.txt", dest / "LICENSES" / f"{content}.txt")
        (dest / ".zenodo.json").write_text(v["ZENODO_JSON"], encoding="utf-8", newline="\n")
    if a.licence != "polyform-nc":
        (dest / "COMMERCIAL.md").unlink()

    left = [
        str(p.relative_to(dest))
        for p in dest.rglob("*")
        if p.is_file() and PLACEHOLDER.search(p.read_text(encoding="utf-8", errors="ignore"))
    ]
    if left:
        sys.exit(f"unfilled placeholders in: {', '.join(left)}")

    subprocess.run(["git", "init", "-q", "-b", "main", str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "config", "user.name", site["author"]], check=True)
    print(f"Created {dest} ({a.kind}, {v['LICENSE_SPDX']}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
