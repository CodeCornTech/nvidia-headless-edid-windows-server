#!/usr/bin/env python3
"""Refresh the self-hosted GitHub stars badge using the GitHub REST API.

No third-party badge host or non-standard Python dependencies are required.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

REPOSITORY = "CodeCornTech/nvidia-headless-edid-windows-server"
BADGE = Path(__file__).resolve().parent.parent / "assets" / "badges" / "stars.svg"


def render_badge(count: int) -> str:
    """Produce a small, self-contained SVG for the nonnegative star count."""
    if type(count) is not int or count < 0:
        raise ValueError("GitHub stars must be a nonnegative integer")
    label = "GitHub Stars"
    value = str(count)
    left = max(47, round(len(label) * 6.3 + 20))
    right = max(31, round(len(value) * 6.3 + 19))
    total = left + right
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="22" '
        f'viewBox="0 0 {total} 22" role="img" aria-label="GitHub Stars: {value}">\n'
        f'  <rect width="{total}" height="22" rx="4" fill="#252b36"/>\n'
        f'  <path d="M{left} 0H{total-4}Q{total} 0 {total} 4V18Q{total} 22 {total-4} 22H{left}Z" '
        f'fill="#a47521"/>\n'
        f'  <text x="{left/2}" y="15.3" fill="#ffffff" font-size="11" '
        f'font-family="Verdana,Geneva,sans-serif" text-anchor="middle">GitHub Stars</text>\n'
        f'  <text x="{left+right/2}" y="15.3" fill="#ffffff" font-size="11" '
        f'font-family="Verdana,Geneva,sans-serif" text-anchor="middle">{value}</text>\n'
        '</svg>\n'
    )


def fetch_stars() -> int:
    """Read the GitHub API with a token; fail closed on any response error."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CodeCornTech-README-stars",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{REPOSITORY}", headers=headers)
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)
    count = payload.get("stargazers_count")
    if type(count) is not int or count < 0:
        raise ValueError("GitHub returned an invalid star count")
    return count


def main() -> None:
    count = fetch_stars()
    rendered = render_badge(count)
    current = BADGE.read_text(encoding="utf-8") if BADGE.exists() else None
    if rendered != current:
        BADGE.parent.mkdir(parents=True, exist_ok=True)
        BADGE.write_text(rendered, encoding="utf-8")
    print(f"GitHub stars: {count}; badge {'unchanged' if rendered == current else 'updated'}")


if __name__ == "__main__":
    main()
