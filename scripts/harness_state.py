#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


CONTEXT_FILES = {
    "facts.md": "# Facts\n",
    "architecture.md": "# Architecture\n",
    "commands.md": "# Commands\n",
    "constraints.md": "# Constraints\n",
    "decisions.md": "# Decisions\n",
    "pitfalls.md": "# Pitfalls\n",
    "links.md": "# Links\n",
    "glossary.md": "# Glossary\n",
}

PROJECT_FILES = {
    "goal.md": "# Goal\n\n",
    "mode.md": "# Mode\n\nmixed\n",
    "status.md": "# Status\n\ncreated\n",
    "next-actions.md": "# Next Actions\n\n- Clarify goal and choose Harness mode.\n",
    "handoff.md": "# Handoff\n\nNo handoff yet.\n",
    "transcript.md": "# Transcript\n\n",
    "research/inventory.md": "# Research Inventory\n\n",
    "research/evidence.md": "# Evidence\n\n",
    "research/analysis.md": "# Analysis\n\n",
    "research/options.md": "# Options\n\n",
    "research/recommendation.md": "# Recommendation\n\n",
    "planning/spec.md": "# Spec\n\n",
    "planning/plan.md": "# Plan\n\n",
    "planning/plan.json": "{\n  \"tasks\": []\n}\n",
    "implementation/changes.md": "# Changes\n\n",
    "implementation/verification.md": "# Verification\n\n",
    "reviews/codex-plan-review.md": "# Codex Plan Review\n\n",
    "reviews/codex-final-review.md": "# Codex Final Review\n\n",
}


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def timestamp() -> str:
    return now().strftime("%Y%m%d-%H%M%S")


def harness_root(cwd: Path) -> Path:
    return cwd / ".harness"


def ensure_structure(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "context" / "lessons").mkdir(parents=True, exist_ok=True)
    (root / "projects").mkdir(parents=True, exist_ok=True)

    config = root / "config.yaml"
    if not config.exists():
        config.write_text(
            "version: 1\n"
            "codex_gates:\n"
            "  plan: medium\n"
            "  final: medium\n"
            "models:\n"
            "  claude_main: deepseek-v4-pro[1M]\n"
            "  claude_cheap: deepseek-v4-flash[1M]\n"
            "  codex_gate: gpt-5.5\n",
            encoding="utf-8",
        )

    index = root / "index.md"
    if not index.exists():
        index.write_text("# Harness Projects\n\n", encoding="utf-8")

    for name, content in CONTEXT_FILES.items():
        path = root / "context" / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def active_project_id(root: Path) -> str | None:
    active = root / "active-project"
    if not active.exists():
        return None
    value = active.read_text(encoding="utf-8").strip()
    return value or None


def project_path(root: Path, project_id: str) -> Path:
    return root / "projects" / project_id


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def create_project(root: Path, goal: str) -> Path:
    project_id = f"project-{timestamp()}"
    path = project_path(root, project_id)
    for rel, content in PROJECT_FILES.items():
        write_if_missing(path / rel, content)

    goal_text = goal.strip() or "No goal provided yet."
    (path / "goal.md").write_text(f"# Goal\n\n{goal_text}\n", encoding="utf-8")
    (path / "transcript.md").write_text(
        f"# Transcript\n\n## {now().isoformat(timespec='seconds')}\n\nCreated project.\n",
        encoding="utf-8",
    )
    (root / "active-project").write_text(project_id + "\n", encoding="utf-8")

    with (root / "index.md").open("a", encoding="utf-8") as fh:
        fh.write(f"- {project_id}: {goal_text}\n")

    return path


def read_trimmed(path: Path, limit: int = 2400) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[trimmed]"


def active_project(root: Path) -> Path | None:
    project_id = active_project_id(root)
    if not project_id:
        return None
    path = project_path(root, project_id)
    return path if path.exists() else None


def render_status(root: Path) -> str:
    project = active_project(root)
    if not project:
        return "No active Harness project. Run /harness <goal> to create one."

    parts = [
        f"Harness active project: {project.name}",
        "",
        "## Goal",
        read_trimmed(project / "goal.md", 1200),
        "",
        "## Status",
        read_trimmed(project / "status.md", 1200),
        "",
        "## Next Actions",
        read_trimmed(project / "next-actions.md", 1200),
        "",
        "## Handoff",
        read_trimmed(project / "handoff.md", 1600),
    ]
    return "\n".join(parts).strip()


def render_context(root: Path) -> str:
    project = active_project(root)
    if not project:
        return ""

    context_root = root / "context"
    snippets = []
    for name in ["constraints.md", "decisions.md", "pitfalls.md", "links.md", "commands.md"]:
        text = read_trimmed(context_root / name, 1000)
        if text and text != CONTEXT_FILES.get(name, "").strip():
            snippets.append(f"## context/{name}\n{text}")

    return (
        "<harness-context>\n"
        "A Harness project is active in this repository. Use /harness-status before resuming substantial work.\n\n"
        f"{render_status(root)}\n\n"
        + ("\n\n".join(snippets) if snippets else "No project memory beyond the active project files yet.")
        + "\n</harness-context>"
    )


def start(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root)

    goal = args.goal.strip()
    active = active_project(root)
    should_resume = goal and any(token in goal for token in ["继续", "resume", "上次", "之前"])

    if active and should_resume:
        print(render_status(root))
        return

    if active and not goal:
        print(render_status(root))
        return

    project = create_project(root, goal)
    print(f"Created Harness project: {project.name}")
    print("")
    print(render_status(root))


def resume(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root)

    query = args.query.strip()
    if query:
        projects = sorted((root / "projects").glob("project-*"), reverse=True)
        matches = [p for p in projects if query in p.name or query in read_trimmed(p / "goal.md", 500)]
        if len(matches) == 1:
            (root / "active-project").write_text(matches[0].name + "\n", encoding="utf-8")
        elif len(matches) > 1:
            print("Multiple matching Harness projects:")
            for item in matches[:10]:
                print(f"- {item.name}: {read_trimmed(item / 'goal.md', 160).replace(chr(10), ' ')}")
            return

    print(render_status(root))


def status(args: argparse.Namespace) -> None:
    root = harness_root(Path(args.cwd).resolve())
    if not root.exists():
        print("No .harness directory in this repository.")
        return
    print(render_status(root))


def session_context(args: argparse.Namespace) -> None:
    root = harness_root(Path(args.cwd).resolve())
    if not root.exists():
        return
    print(render_context(root))


def stop(args: argparse.Namespace) -> None:
    root = harness_root(Path(args.cwd).resolve())
    project = active_project(root) if root.exists() else None
    if not project:
        return

    stamp = now().isoformat(timespec="seconds")
    transcript = project / "transcript.md"
    with transcript.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {stamp}\n\nClaude Code session stopped.\n")

    handoff = project / "handoff.md"
    if handoff.exists() and "No handoff yet." in handoff.read_text(encoding="utf-8", errors="replace"):
        handoff.write_text(
            "# Handoff\n\n"
            "Update this before stopping substantial work:\n\n"
            "- What changed:\n"
            "- Current state:\n"
            "- Blockers:\n"
            "- Next recommended action:\n",
            encoding="utf-8",
        )

    print("Harness stop hook ran. Ensure handoff.md, status.md, and next-actions.md are current before relying on resume.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage project-local Harness state.")
    sub = parser.add_subparsers(dest="command", required=True)

    start_cmd = sub.add_parser("start")
    start_cmd.add_argument("--cwd", required=True)
    start_cmd.add_argument("--goal", default="")
    start_cmd.set_defaults(func=start)

    resume_cmd = sub.add_parser("resume")
    resume_cmd.add_argument("--cwd", required=True)
    resume_cmd.add_argument("--query", default="")
    resume_cmd.set_defaults(func=resume)

    status_cmd = sub.add_parser("status")
    status_cmd.add_argument("--cwd", required=True)
    status_cmd.set_defaults(func=status)

    context_cmd = sub.add_parser("session-context")
    context_cmd.add_argument("--cwd", required=True)
    context_cmd.set_defaults(func=session_context)

    stop_cmd = sub.add_parser("stop")
    stop_cmd.add_argument("--cwd", required=True)
    stop_cmd.set_defaults(func=stop)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
