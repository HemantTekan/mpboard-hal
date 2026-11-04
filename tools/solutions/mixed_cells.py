#!/usr/bin/env python3
"""Equation helpers whose cells may mix Hindi \\text{...} with TeX (chapters 5 onwards).

Import after common:  from common import *  then  from mixed_cells import *
These `lines` and `eqs` replace the plain versions from common.
"""
import re as _re
from common import mcell

__all__ = ["mc", "lines", "eqs"]

_DEV = _re.compile(r"[\u0900-\u097F]")


def mc(c):
    """Cell that may mix Hindi \\text{..} with maths: Hindi stays plain text, the rest is TeX."""
    c = str(c)
    if not _DEV.search(c):
        return mcell(c)
    out = []
    for i, piece in enumerate(_re.split(r"\\text\{([^}]*)\}", c)):
        if i % 2:
            out.append(piece)
        elif piece.strip().strip("\\").strip():
            out.append("\\(" + piece.strip().rstrip("\\").strip() + "\\)")
    return " ".join(out)


def lines(head, *rest):
    """First line 'LHS = RHS', then each further '= ...' aligned under the first '='."""
    head, rest = mc(head), [mc(r) for r in rest]
    out = f"<span class='l'>{head}</span><span class='s'>=</span><span class='r'>{rest[0]}</span>"
    out += "".join(f"<span class='l'></span><span class='s'>=</span><span class='r'>{r}</span>" for r in rest[1:])
    return "<div class='eq'>" + out + "</div>"


def eqs(*pairs):
    """Separate equations, one per row, aligned at '='."""
    rows = "".join(f"<span class='l'>{mc(a)}</span><span class='s'>=</span><span class='r'>{mc(b)}</span>" for a, b in pairs)
    return "<div class='eq'>" + rows + "</div>"
