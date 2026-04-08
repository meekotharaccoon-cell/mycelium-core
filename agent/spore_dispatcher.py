#!/usr/bin/env python3
"""
mycelium-core :: Spore Dispatcher
==================================
When the orchestrator detects gaps (stale repos, failing workflows),
the spore dispatcher creates targeted issues or triggers workflow_dispatch
events on those repos to kick them back into action.

Priority tiers:
  CRITICAL  -- security / money (mycelium-money, solarpunk-bank)
  GROWTH    -- visibility / grants (mycelium-visibility, mycelium-grants, solarpunk-grants)
  MAINTENANCE -- everything else
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ORG = "meekotharaccoon-cell"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DISPATCHES_PATH = DATA_DIR / "dispatches.json"

PRIORITY_MAP = {
    "mycelium-money":       "critical",
    "solarpunk-bank":       "critical",
    "solarpunk-legal":      "critical",
    "mycelium-visibility":  "growth",
    "mycelium-grants":      "growth",
    "solarpunk-grants":     "growth",
    "solarpunk-market":     "growth",
    "gaza-rose-gallery":    "growth",
}
DEFAULT_PRIORITY = "maintenance"

PRIORITY_ORDER = {"critical": 0, "growth": 1, "maintenance": 2}


# -- helpers --

def gh_cli(args: list[str]) -> str | None:
    """Run a gh CLI command, return stdout."""
    try:
        result = subprocess.run(
            ["gh"] + args, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        return None


def load_dispatches() -> list[dict]:
    """Load existing dispatch log."""
    if DISPATCHES_PATH.exists():
        try:
            return json.loads(DISPATCHES_PATH.read_text())
        except json.JSONDecodeError:
            return []
    return []


def save_dispatches(dispatches: list[dict]):
    """Persist dispatch log."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DISPATCHES_PATH.write_text(json.dumps(dispatches, indent=2))


def repo_short(full_name: str) -> str:
    """Extract repo name from org/repo."""
    return full_name.split("/")[-1] if "/" in full_name else full_name


def get_priority(repo: str) -> str:
    short = repo_short(repo)
    return PRIORITY_MAP.get(short, DEFAULT_PRIORITY)


# -- dispatch actions --

def create_nudge_issue(repo: str, status: str, details: dict) -> dict | None:
    """Create an issue on the target repo asking it to wake up."""
    short = repo_short(repo)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    priority = get_priority(repo)

    title = f"[Mycelium Spore] {status.upper()} -- needs attention ({now})"

    body_parts = [
        f"## Spore Dispatch -- Priority: `{priority}`\n",
        f"The mycelium-core orchestrator flagged **{repo}** as **{status}**.\n",
    ]

    if details.get("days_ago") is not None:
        body_parts.append(f"- Last commit: **{details['days_ago']}** days ago")
    if details.get("failing"):
        wf = details.get("workflow", {})
        body_parts.append(f"- Workflow `{wf.get('name', 'unknown')}` conclusion: `{wf.get('conclusion', 'unknown')}`")
        if wf.get("html_url"):
            body_parts.append(f"- Run: {wf['html_url']}")

    body_parts.append(f"\n**Action needed:** investigate and resolve.\n")
    body_parts.append("---\n_Auto-dispatched by mycelium-core spore dispatcher._")

    body = "\n".join(body_parts)

    result = gh_cli([
        "issue", "create",
        "--repo", f"{ORG}/{short}",
        "--title", title,
        "--body", body,
        "--label", "spore-dispatch",
    ])

    if result:
        print(f"  [{priority.upper()}] Issue created on {short}: {result}")
        return {
            "repo": repo,
            "action": "issue_created",
            "priority": priority,
            "status": status,
            "issue_url": result,
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
        }
    else:
        print(f"  [{priority.upper()}] Failed to create issue on {short}")
        return None


def trigger_workflow(repo: str, workflow_file: str = "main.yml") -> dict | None:
    """Trigger workflow_dispatch on target repo if it has the workflow."""
    short = repo_short(repo)
    priority = get_priority(repo)

    result = gh_cli([
        "workflow", "run", workflow_file,
        "--repo", f"{ORG}/{short}",
    ])

    if result is not None:
        print(f"  [{priority.upper()}] Triggered {workflow_file} on {short}")
        return {
            "repo": repo,
            "action": "workflow_dispatch",
            "priority": priority,
            "workflow": workflow_file,
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
        }
    else:
        print(f"  [{priority.upper()}] No dispatchable workflow on {short}, skipping trigger")
        return None


# -- main dispatch logic --

def dispatch_from_health(health_path: Path | None = None):
    """Read the health report and dispatch spores to sick repos."""
    if health_path is None:
        health_path = DATA_DIR / "organism_health.json"

    if not health_path.exists():
        print("No health report found. Run orchestrator first.")
        sys.exit(1)

    report = json.loads(health_path.read_text())
    repos = report.get("repos", [])

    # filter to problems, sort by priority
    problems = [r for r in repos if r["status"] != "healthy"]
    problems.sort(key=lambda r: PRIORITY_ORDER.get(get_priority(r["repo"]), 99))

    if not problems:
        print("All repos healthy. Nothing to dispatch.")
        return

    print(f"=== Spore Dispatcher: {len(problems)} repo(s) need attention ===\n")

    dispatches = load_dispatches()
    new_dispatches = []

    for repo_info in problems:
        repo = repo_info["repo"]
        status = repo_info["status"]

        # create nudge issue
        d = create_nudge_issue(repo, status, repo_info)
        if d:
            new_dispatches.append(d)

        # if failing, also try to trigger a fresh workflow run
        if repo_info.get("failing"):
            d2 = trigger_workflow(repo)
            if d2:
                new_dispatches.append(d2)

    # persist
    dispatches.extend(new_dispatches)
    save_dispatches(dispatches)
    print(f"\n  {len(new_dispatches)} dispatch(es) logged to {DISPATCHES_PATH}")


if __name__ == "__main__":
    dispatch_from_health()
