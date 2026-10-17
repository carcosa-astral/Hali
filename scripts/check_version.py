#!/usr/bin/env python3
"""Check that every place that states the Hali version agrees with the VERSION file.

Run from the repository root:

    python3 scripts/check_version.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def main():
    version = read("VERSION").strip()
    problems = []

    if not re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?", version):
        problems.append("VERSION is not valid SemVer: %r" % version)

    pkg = json.loads(read("package.json"))
    if pkg.get("version") != version:
        problems.append("package.json version %s != VERSION %s" % (pkg.get("version"), version))

    tokens = json.loads(read("tokens/hali-tokens.json"))
    if tokens["$meta"].get("version") != version:
        problems.append("tokens/hali-tokens.json version %s != VERSION %s (run build_tokens.py)"
                        % (tokens["$meta"].get("version"), version))

    for sprite in ("icons/hali-icons.svg", "icons/hali-icons-16.svg"):
        m = re.search(r"Hali (?:16px )?icons v(\d+\.\d+\.\d+)", read(sprite))
        if not m or m.group(1) != version:
            problems.append("%s header version %s != VERSION %s" % (sprite, m.group(1) if m else "missing", version))

    css = read("css/hali.css")
    m = re.search(r"Hali design language v(\S+)", css)
    if not m or m.group(1) != version:
        problems.append("css/hali.css header version %s != VERSION %s" % (m.group(1) if m else "missing", version))

    js = read("js/hali.js")
    m = re.search(r"Hali design language v(\S+)", js)
    if not m or m.group(1) != version:
        problems.append("js/hali.js header version %s != VERSION %s" % (m.group(1) if m else "missing", version))
    m = re.search(r"var VERSION = '([^']+)'", js)
    if not m or m.group(1) != version:
        problems.append("js/hali.js VERSION constant %s != VERSION %s" % (m.group(1) if m else "missing", version))

    tokens_css = read("tokens/hali-tokens.css")
    m = re.search(r"Hali design language v(\S+) tokens", tokens_css)
    if not m or m.group(1) != version:
        problems.append("tokens/hali-tokens.css header version %s != VERSION %s (run build_tokens.py)"
                        % (m.group(1) if m else "missing", version))

    changelog = read("CHANGELOG.md")
    if not re.search(r"^## \[%s\] - \d{4}-\d{2}-\d{2}" % re.escape(version), changelog, re.M):
        problems.append("CHANGELOG.md has no dated entry for %s" % version)

    if problems:
        for p in problems:
            print("FAIL " + p)
        return 1
    print("Version %s is consistent across VERSION, package.json, tokens, CSS and CHANGELOG." % version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
