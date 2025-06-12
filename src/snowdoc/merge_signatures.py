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
    return "\n".join((indent + ln.lstrip() if ln.strip() else ln) for ln in lines)


def loose_regex(anchor_line: str) -> re.Pattern:
    """
    Build a forgiving regex from an anchor line:

    * Collapse each run of whitespace to  `\\s+`
    * Escape all regex metacharacters
    * Ignore everything after the first ‘{’ (so matching works even if
      the brace is on the next line in the source file)
    * Anchor at line start (allow preceding spaces)
    """
    head = anchor_line.split("{", 1)[0]      #  everything before first '{'
    escaped = SPECIAL_RE.sub(lambda m: "\\" + m.group(0), head)
    collapsed = re.sub(r"\s+", r"\\s+", escaped)
    return re.compile(r"^\s*" + collapsed)


def extract_pairs(text: str) -> List[Tuple[re.Pattern, str]]:
    """
    Return [(anchor_regex, comment_block), …]  for every JSDoc block found.
    """
    pairs = []
    for m in COMMENT_RE.finditer(text):
        comment = m.group(0).rstrip()
        after = text[m.end():]
        # first non-empty, non-whitespace line
        anchor = next((ln for ln in after.splitlines() if ln.strip()), None)
        if not anchor:
            continue
        pairs.append((loose_regex(anchor), comment))
    return pairs


def inject_docs(pairs: List[Tuple[re.Pattern, str]], source_text: str) -> str:
    """
    Stream-merge the doc blocks into the source file.
    """
    used = [False] * len(pairs)
    out_lines = []

    for line in source_text.splitlines():
        # does this line match any *unused* anchor?
        try:
            idx = next(i for i, (rx, _) in enumerate(pairs) if not used[i] and rx.match(line))
        except StopIteration:
            idx = None

        if idx is not None:
            indent_match = re.match(r"^(\s*)", line)
            indent = indent_match.group(1) if indent_match else ""
            out_lines.append(_indent_block(pairs[idx][1], indent))   # emit indented JSDoc before the code line
            used[idx] = True

        out_lines.append(line)

    # any leftovers?
    for (rx, comment), was_used in zip(pairs, used):
        if not was_used:
            out_lines.extend([
                "",
                "// TODO: Could not automatically inject the following doc block:",
                comment
            ])

    return "\n".join(out_lines)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage:\n  python merge_signatures.py <signature.js> <source.js>", file=sys.stderr)
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
