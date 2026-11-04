#!/usr/bin/env python3
"""Geometry helpers (chapters 6 onwards): दिया है / सिद्ध करना है boxes, उपपत्ति rows,
inline symbols and a small SVG figure builder.

Import after common:  from geometry import *
"""
from common import m

__all__ = ["gp", "pf", "r", "T", "A", "fig"]


def gp(dia, sid, extra=None):
    """दिया है / सिद्ध करना है boxes."""
    h = (f"<div class='gv'><div class='box k'><b>दिया है</b><div>{dia}</div></div>"
         f"<div class='box f'><b>{'सिद्ध करना है' if extra is None else extra}</b><div>{sid}</div></div></div>")
    return h


def pf(*rows):
    """उपपत्ति: each row is (statement, reason); the reason sits on its own small line."""
    out = "<div class='vt'>उपपत्ति:</div><div style='margin:6px 0 4px'>"
    for st, rs in rows:
        out += ("<div style='padding:6px 0;border-bottom:1px dashed #e3e7f3'>"
                f"<div>{st}</div>" + (f"<div style='font-size:.88em;color:#5a6275'>({rs})</div>" if rs else "") + "</div>")
    return out + "</div>"


def r(a, b):
    """Inline ratio a/b."""
    return m(f"\\dfrac{{{a}}}{{{b}}}")


def T(x):
    """Inline triangle: T("ABC") -> ΔABC."""
    return m("\\triangle " + x)


def A(x):
    """Inline angle: A("ABC") -> ∠ABC."""
    return m("\\angle " + x)


def fig(W, H, pts, segs, dashed=(), labels=(), extra="", caption=""):
    """Small geometry figure. pts: name -> (x, y, dx, dy) where (dx, dy) shifts the letter."""
    g = [f"<svg class='graph' viewBox='0 0 {W} {H}' role='img' aria-label='{caption or 'आकृति'}' style='max-width:{min(W, 340)}px'>"]
    for a, b in segs:
        (x1, y1, *_), (x2, y2, *_) = pts[a], pts[b]
        g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#1d3a8a' stroke-width='2'/>")
    for a, b in dashed:
        (x1, y1, *_), (x2, y2, *_) = pts[a], pts[b]
        g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#c2410c' stroke-width='1.8' stroke-dasharray='5 4'/>")
    g.append(extra)
    for n, (x, y, dx, dy) in pts.items():
        g.append(f"<circle cx='{x}' cy='{y}' r='2.6' fill='#1d3a8a'/><text x='{x + dx}' y='{y + dy}' font-size='15' font-weight='700' fill='#111' text-anchor='middle'>{n}</text>")
    for x, y, t in labels:
        g.append(f"<text x='{x}' y='{y}' font-size='12.5' fill='#b4232a' text-anchor='middle'>{t}</text>")
    g.append("</svg>")
    cap = f"<div style='font-size:.85em;color:#5a6275;margin-top:2px'>{caption}</div>" if caption else ""
    return "<div style='margin:8px 0'>" + "".join(g) + cap + "</div>"
