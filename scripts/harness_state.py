#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


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

EVENT_COUNTER_KEYS = {
    "user-prompts.jsonl": "user_prompts",
    "tool-uses.jsonl": "tool_uses",
    "tool-failures.jsonl": "tool_failures",
    "file-changes.jsonl": "file_changes",
    "session-events.jsonl": "session_events",
}

HIGH_VALUE_PROMPT_PATTERNS = [
    "记住",
    "以后",
    "不要",
    "不是这样",
    "不对",
    "错了",
    "应该",
    "这个链接",
    "文档",
    "之前",
    "别再",
    "踩坑",
    "根因",
]


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def iso_now() -> str:
    return now().isoformat(timespec="seconds")


def timestamp() -> str:
    return now().strftime("%Y%m%d-%H%M%S")


def run_git(cwd: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2,
        )
    except Exception:
        return ""
    return result.stdout.strip()


def git_root(cwd: Path) -> Path:
    root = run_git(cwd, ["rev-parse", "--show-toplevel"])
    return Path(root).resolve() if root else cwd.resolve()


def git_remote(cwd: Path) -> str:
    return run_git(cwd, ["remote", "get-url", "origin"])


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return value[:48] or "repo"


def repo_identity(cwd: Path) -> dict[str, str]:
    repo_root = git_root(cwd)
    remote = git_remote(repo_root)
    identity_source = f"{repo_root}\n{remote}"
    digest = hashlib.sha1(identity_source.encode("utf-8")).hexdigest()[:12]
    repo_id = f"{slugify(repo_root.name)}-{digest}"
    return {
        "id": repo_id,
        "cwd": str(cwd.resolve()),
        "repo_root": str(repo_root),
        "remote": remote,
    }


def harness_home() -> Path:
    return Path(os.environ.get("HARNESS_HOME", "~/.harness")).expanduser().resolve()


def harness_root(cwd: Path) -> Path:
    """Return the default global Harness root for this repository.

    Project-local .harness is intentionally no longer the default. It can be
    reintroduced later as an explicit export/localize operation.
    """

    return harness_home() / "projects" / repo_identity(cwd)["id"]


def ensure_structure(root: Path, cwd: Path | None = None) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "context" / "lessons").mkdir(parents=True, exist_ok=True)
    (root / "events").mkdir(parents=True, exist_ok=True)
    (root / "projects").mkdir(parents=True, exist_ok=True)

    config = root / "config.yaml"
    if not config.exists():
        config.write_text(
            "version: 2\n"
            "storage: global\n"
            "events:\n"
            "  enabled: true\n"
            "  compactor: external\n"
            "models:\n"
            "  compactor: minimax-or-cheap-model\n"
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

    state = root / "state.json"
    if not state.exists():
        state.write_text(
            json.dumps(
                {
                    "version": 1,
                    "created_at": iso_now(),
                    "last_seen_at": iso_now(),
                    "pending": {
                        "user_prompts": 0,
                        "tool_uses": 0,
                        "tool_failures": 0,
                        "file_changes": 0,
                        "session_events": 0,
                        "high_value_prompts": 0,
                    },
                    "last_compacted_at": None,
                    "compactor_running": False,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    if cwd is not None:
        identity = repo_identity(cwd)
        repo = {
            **identity,
            "memory_root": str(root),
            "last_seen_at": iso_now(),
        }
        (root / "repo.json").write_text(
            json.dumps(repo, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_trimmed(path: Path, limit: int = 2400) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[trimmed]"


def is_empty_context_file(name: str, text: str) -> bool:
    return text.strip() == CONTEXT_FILES.get(name, "").strip()


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
        f"# Transcript\n\n## {iso_now()}\n\nCreated project.\n",
        encoding="utf-8",
    )
    (root / "active-project").write_text(project_id + "\n", encoding="utf-8")

    with (root / "index.md").open("a", encoding="utf-8") as fh:
        fh.write(f"- {project_id}: {goal_text}\n")

    return path


def active_project(root: Path) -> Path | None:
    project_id = active_project_id(root)
    if not project_id:
        return None
    path = project_path(root, project_id)
    return path if path.exists() else None


def render_status(root: Path) -> str:
    project = active_project(root)
    repo = read_json(root / "repo.json")
    parts = [
        f"Harness memory root: {root}",
        f"Repo: {repo.get('repo_root', '(unknown)')}",
    ]

    if not project:
        parts.append("")
        parts.append("No active Harness workflow project. Memory hooks still record raw events.")
        return "\n".join(parts).strip()

    parts.extend(
        [
            "",
            f"Harness active workflow project: {project.name}",
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
    )
    return "\n".join(parts).strip()


def render_context(root: Path) -> str:
    context_root = root / "context"
    snippets = []
    for name, limit in [
        ("facts.md", 800),
        ("architecture.md", 900),
        ("constraints.md", 700),
        ("decisions.md", 700),
        ("pitfalls.md", 900),
        ("links.md", 700),
        ("commands.md", 800),
    ]:
        text = read_trimmed(context_root / name, limit)
        if text and not is_empty_context_file(name, text):
            snippets.append(f"## context/{name}\n{text}")

    repo = read_json(root / "repo.json")
    body = "\n\n".join(snippets) if snippets else "No durable project memory has been compacted yet."
    return (
        "<harness-memory>\n"
        "Harness is enabled as a global Claude Code memory layer. It records raw events in the background and injects compacted project memory here.\n"
        f"Memory root: {root}\n"
        f"Repo root: {repo.get('repo_root', '(unknown)')}\n"
        "Use this memory before rescanning the whole project. If you discover durable facts, commands, pitfalls, decisions, constraints, or links, preserve them in the memory root.\n\n"
        f"{body}\n"
        "</harness-memory>"
    )


def prompt_is_high_value(prompt: str) -> bool:
    return any(pattern in prompt for pattern in HIGH_VALUE_PROMPT_PATTERNS)


def result_failed(tool_result: Any) -> bool:
    if isinstance(tool_result, dict):
        for key in ["is_error", "error", "failed"]:
            value = tool_result.get(key)
            if value is True:
                return True
        for key in ["exit_code", "exitCode", "status"]:
            value = tool_result.get(key)
            if isinstance(value, int) and value != 0:
                return True
            if isinstance(value, str) and value.isdigit() and int(value) != 0:
                return True
    text = json.dumps(tool_result, ensure_ascii=False) if not isinstance(tool_result, str) else tool_result
    lower = text.lower()
    return bool(
        re.search(r"exit code\s+[1-9]\d*", lower)
        or re.search(r"exited with code\s+[1-9]\d*", lower)
        or "traceback (most recent call last)" in lower
        or "error:" in lower
        or "failed" in lower
    )


def normalize_event(event_name: str, cwd: Path, payload: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    identity = repo_identity(cwd)
    row: dict[str, Any] = {
        "ts": iso_now(),
        "event": event_name,
        "repo_id": identity["id"],
        "repo_root": identity["repo_root"],
        "cwd": payload.get("cwd") or str(cwd.resolve()),
        "session_id": payload.get("session_id"),
        "transcript_path": payload.get("transcript_path"),
    }
    files = ["session-events.jsonl"]

    if event_name == "UserPromptSubmit":
        prompt = payload.get("user_prompt") or payload.get("prompt") or ""
        row["user_prompt"] = prompt
        row["high_value"] = prompt_is_high_value(prompt)
        files = ["user-prompts.jsonl"]
    elif event_name == "PostToolUse":
        tool_name = payload.get("tool_name")
        tool_input = payload.get("tool_input")
        tool_result = payload.get("tool_result")
        failed = result_failed(tool_result)
        row.update(
            {
                "tool_name": tool_name,
                "tool_input": tool_input,
                "tool_failed": failed,
                "tool_result_preview": read_result_preview(tool_result),
            }
        )
        files = ["tool-uses.jsonl"]
        if failed:
            files.append("tool-failures.jsonl")
        if tool_name in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
            row["file_path"] = extract_file_path(tool_input)
            files.append("file-changes.jsonl")
    elif event_name in {"PreCompact", "SessionEnd", "Stop", "SessionStart", "SubagentStop"}:
        row["reason"] = payload.get("reason")
        if "agent_id" in payload:
            row["agent_id"] = payload.get("agent_id")
        if "agent_transcript_path" in payload:
            row["agent_transcript_path"] = payload.get("agent_transcript_path")

    return files, row


def read_result_preview(tool_result: Any, limit: int = 2000) -> str:
    text = tool_result if isinstance(tool_result, str) else json.dumps(tool_result, ensure_ascii=False)
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n...[trimmed]"


def extract_file_path(tool_input: Any) -> str | None:
    if isinstance(tool_input, dict):
        for key in ["file_path", "path", "notebook_path"]:
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    return None


def update_pending_counts(root: Path, files: list[str], row: dict[str, Any]) -> None:
    state_path = root / "state.json"
    state = read_json(state_path)
    pending = state.setdefault("pending", {})
    for filename in files:
        key = EVENT_COUNTER_KEYS.get(filename)
        if key:
            pending[key] = int(pending.get(key, 0) or 0) + 1
    if row.get("high_value"):
        pending["high_value_prompts"] = int(pending.get("high_value_prompts", 0) or 0) + 1
    state["last_seen_at"] = iso_now()
    state["last_event_at"] = row["ts"]
    state["needs_compaction"] = should_compact(pending, state)
    write_json(state_path, state)


def should_compact(pending: dict[str, Any], state: dict[str, Any]) -> bool:
    if int(pending.get("high_value_prompts", 0) or 0) >= 1:
        return True
    if int(pending.get("tool_failures", 0) or 0) >= 2:
        return True
    if int(pending.get("file_changes", 0) or 0) >= 5:
        return True
    total = sum(int(v or 0) for v in pending.values() if isinstance(v, int))
    return total >= 20 or bool(state.get("force_compaction"))


def record_event(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    event_name = args.event or payload.get("hook_event_name") or "Unknown"
    files, row = normalize_event(event_name, cwd, payload)
    for filename in files:
        append_jsonl(root / "events" / filename, row)
    update_pending_counts(root, files, row)
    print("{}")


def start(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)

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
    print(f"Created Harness workflow project: {project.name}")
    print(f"Memory root: {root}")
    print("")
    print(render_status(root))


def resume(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)

    query = args.query.strip()
    if query:
        projects = sorted((root / "projects").glob("project-*"), reverse=True)
        matches = [p for p in projects if query in p.name or query in read_trimmed(p / "goal.md", 500)]
        if len(matches) == 1:
            (root / "active-project").write_text(matches[0].name + "\n", encoding="utf-8")
        elif len(matches) > 1:
            print("Multiple matching Harness workflow projects:")
            for item in matches[:10]:
                print(f"- {item.name}: {read_trimmed(item / 'goal.md', 160).replace(chr(10), ' ')}")
            return

    print(render_status(root))


def status(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)
    print(render_status(root))


def root_path(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)
    print(root)


def session_context(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)
    print(render_context(root))


def stop(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd).resolve()
    root = harness_root(cwd)
    ensure_structure(root, cwd)

    row = {
        "ts": iso_now(),
        "event": "Stop",
        "repo_id": repo_identity(cwd)["id"],
        "repo_root": repo_identity(cwd)["repo_root"],
        "cwd": str(cwd),
        "reason": "Claude Code stop hook",
    }
    append_jsonl(root / "events" / "session-events.jsonl", row)
    update_pending_counts(root, ["session-events.jsonl"], row)

    project = active_project(root)
    if project:
        transcript = project / "transcript.md"
        with transcript.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## {iso_now()}\n\nClaude Code session stopped.\n")

    print(f"Harness memory root: {root}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage global Harness memory state.")
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

    root_cmd = sub.add_parser("root")
    root_cmd.add_argument("--cwd", required=True)
    root_cmd.set_defaults(func=root_path)

    context_cmd = sub.add_parser("session-context")
    context_cmd.add_argument("--cwd", required=True)
    context_cmd.set_defaults(func=session_context)

    event_cmd = sub.add_parser("record-event")
    event_cmd.add_argument("--cwd", required=True)
    event_cmd.add_argument("--event", default="")
    event_cmd.set_defaults(func=record_event)

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
