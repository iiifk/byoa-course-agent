from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
from urllib.request import Request, urlopen


@dataclass
class GitHubInfo:
    url: str
    title: str | None
    status: str


def read_text_files(paths: Iterable[Path]) -> dict[str, str]:
    """Read lightweight text context files for the agent workspace."""
    result: dict[str, str] = {}
    for path in paths:
        if path.suffix.lower() in {".md", ".txt"} and path.exists():
            result[str(path)] = path.read_text(encoding="utf-8")
    return result


def fetch_github_page(url: str) -> GitHubInfo:
    request = Request(url, headers={"User-Agent": "byoa-course-agent"})
    try:
        with urlopen(request, timeout=10) as response:
            html = response.read(200_000).decode("utf-8", errors="ignore")
        title = None
        if "<title>" in html and "</title>" in html:
            title = html.split("<title>", 1)[1].split("</title>", 1)[0].strip()
        return GitHubInfo(url=url, title=title, status="verified")
    except Exception as exc:
        return GitHubInfo(url=url, title=None, status=f"pending: {exc}")


def build_report_context(workspace: Path) -> dict[str, object]:
    prompt_path = workspace / "byoa-course-agent" / "prompts" / "core_prompt.md"
    context_files = read_text_files([prompt_path, workspace / "README.md"])
    github_urls = [
        "https://github.com/iiifk",
        "https://github.com/firstcontributions/first-contributions/pull/120374",
    ]
    github_info = [asdict(fetch_github_page(url)) for url in github_urls]
    return {
        "workspace": str(workspace),
        "context_files": context_files,
        "github_info": github_info,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build context for course reports.")
    parser.add_argument("--workspace", default=".", help="Course workspace path")
    args = parser.parse_args()
    context = build_report_context(Path(args.workspace).resolve())
    print(json.dumps(context, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

