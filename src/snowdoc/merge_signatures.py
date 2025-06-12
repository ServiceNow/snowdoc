#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from typing import List, Tuple

COMMENT_RE = re.compile(r"/\*\*[\s\S]*?\*/")          # greedy across newlines
SPECIAL_RE = re.compile(r"[-/\\^$*+?.()|[\]{}]")      # chars to escape


def _indent_block(block: str, indent: str) -> str:
    """Prefix every docblock line with *indent*, stripping its original leading spaces to avoid double indent."""
    lines = block.splitlines()
    return "\n".join(
        (indent + ln.lstrip() if ln.strip() else ln)     # preserve blank lines
        for ln in lines
    )

def _dedent_block(block: str) -> str:
    """Left-trim all lines in *block* (used only for TODO leftovers)."""
    return "\n".join(ln.lstrip() for ln in block.splitlines())

def loose_regex(anchor_line: str) -> re.Pattern:
    """
    Build a forgiving regex from an anchor line.

    * Extract just the first identifier (e.g.  `isTableExtended`)
    * Match it anywhere on the line, whether it appears as
        - `isTableExtended: function(`   (object-literal style)
        - `function isTableExtended(`    (stand-alone function)
        - `var isTableExtended = (`      (var/let/const assignment)
    """
    m = re.search(r"[A-Za-z_$][A-Za-z0-9_$]*", anchor_line)
    if not m:                          # fallback: never matches
        return re.compile(r"$^")

    ident = re.escape(m.group(0))
    return re.compile(r"\b" + ident + r"\b", re.IGNORECASE)

def extract_pairs(text: str) -> List[Tuple[re.Pattern, str]]:
    """
    Return [(anchor_regex, comment_block), …]  for every JSDoc block found.
    """
    pairs: List[Tuple[re.Pattern, str]] = []
    for m in COMMENT_RE.finditer(text):
        comment = m.group(0).rstrip()
        after = text[m.end():]

        # first non-empty line after the comment
        anchor = next((ln for ln in after.splitlines() if ln.strip()), None)
        if not anchor:
            continue

        pairs.append((loose_regex(anchor), comment))
    return pairs

def inject_docs(pairs, source_text: str) -> str:
    used = [False] * len(pairs)
    out_lines = []

    for line in source_text.splitlines():
        try:
            idx = next(
                i for i, (rx, _) in enumerate(pairs)
                if not used[i] and rx.search(line)        # <──  changed: .search
            )
        except StopIteration:
            idx = None

        if idx is not None:
            indent = re.match(r"^(\s*)", line).group(1)
            out_lines.append(_indent_block(pairs[idx][1], indent))
            used[idx] = True

        out_lines.append(line)

    # leave leftovers under a TODO banner exactly as before
    for (rx, comment), was_used in zip(pairs, used):
        if not was_used:
            out_lines.extend([
                "",
                "// TODO: Could not automatically inject the following doc block:",
                _dedent_block(comment)            # <──  dedent before appending
            ])
    return "\n".join(out_lines)

def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage:\n  python merge_signatures.py <signature.js> <source.js>",
            file=sys.stderr
        )
        sys.exit(1)

    sig_path = Path(sys.argv[1])
    src_path = Path(sys.argv[2])

    signature_text = sig_path.read_text(encoding="utf-8")
    source_text = src_path.read_text(encoding="utf-8")

    pairs = extract_pairs(signature_text)
    merged = inject_docs(pairs, source_text)
    sys.stdout.write(merged)


if __name__ == "__main__":
    main()
