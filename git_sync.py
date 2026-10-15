"""Pull the latest master into Rain's open repos when a chat starts (hook script).

What it does: for each repo it covers, fetches origin and merges the default
branch (master or main) into the current branch. A merge that would conflict
is aborted, never forced, and reported.

Which repos: the repo of the current folder, the folders listed in its
*.code-workspace file, and ~/.claude (dot-claude).

How to run (the SessionStart hook calls it; reads hook JSON on stdin):
  python git_sync.py
"""
import json
import os
import subprocess
import sys

OWNER = "serina-sketch"


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def repo_root(path):
    code, out = git(path, "rev-parse", "--show-toplevel")
    return os.path.normpath(out) if code == 0 else None


def is_mine(repo):
    code, out = git(repo, "remote", "get-url", "origin")
    return code == 0 and OWNER in out


def find_repos(cwd):
    repos = []
    here = repo_root(cwd)
    if here:
        repos.append(here)
    # The folders open in the VS Code workspace, from any *.code-workspace
    # file at the repo root (paths are relative to that file).
    root = here or os.path.abspath(cwd)
    try:
        for name in os.listdir(root):
            if name.endswith(".code-workspace"):
                with open(os.path.join(root, name), encoding="utf-8") as f:
                    text = "\n".join(l for l in f if not l.lstrip().startswith("//"))
                for folder in json.loads(text).get("folders", []):
                    p = os.path.normpath(os.path.join(root, os.path.expanduser(folder.get("path", ""))))
                    if os.path.isdir(p) and repo_root(p):
                        repos.append(repo_root(p))
    except (OSError, ValueError):
        pass
    home_claude = os.path.join(os.path.expanduser("~"), ".claude")
    if os.path.isdir(os.path.join(home_claude, ".git")):
        repos.append(os.path.normpath(home_claude))
    seen, out = set(), []
    for r in repos:
        if r not in seen and is_mine(r):
            seen.add(r)
            out.append(r)
    return out


def default_branch(repo):
    for b in ("master", "main"):
        if git(repo, "rev-parse", "--verify", "-q", f"origin/{b}")[0] == 0:
            return b
    return None


def sync(repo):
    """Return a message, or None when there was nothing to do."""
    name = os.path.basename(repo)
    code, out = git(repo, "fetch", "-q", "origin")
    if code != 0:
        return f"{name}: fetch failed ({out.splitlines()[-1] if out else 'no output'})"
    base = default_branch(repo)
    if not base:
        return None
    code, behind = git(repo, "rev-list", "--count", f"HEAD..origin/{base}")
    if code != 0 or behind == "0":
        return None
    code, out = git(repo, "merge", "--no-edit", f"origin/{base}")
    if code == 0:
        return f"{name}: pulled {behind} new commit(s) from {base}"
    git(repo, "merge", "--abort")
    return (f"{name}: {base} has {behind} new commit(s) that conflict with "
            f"local changes; merge aborted, nothing changed. Resolve before writing.")


def main():
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    msgs = [m for m in (sync(r) for r in find_repos(cwd)) if m]
    if msgs:
        print("Git sync: " + " | ".join(msgs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
