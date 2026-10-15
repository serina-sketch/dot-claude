"""Keep Rain's repos in sync with GitHub (hook script).

What it does: for each repo it covers, fetches origin and merges the default
branch (master or main) into the current branch. A merge that would conflict
is aborted, never forced, and reported.

Which repos: the repo of the current folder, the folders listed in its
*.code-workspace file, every sibling repo in the same
parent folder whose origin is on serina-sketch's GitHub, and ~/.claude
(dot-claude). This covers VS Code workspaces with several folders open.

How to run (hooks call it; reads hook JSON on stdin when present):
  python git_sync.py start        # SessionStart: sync all, report to Claude
  python git_sync.py pre-tool     # PreToolUse Bash: before git commit/push,
                                  # sync all; block (exit 2) on a conflict
  python git_sync.py post-tool    # PostToolUse Bash: after git push, check
                                  # the repo matches origin
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
    # Fallback: repos in the same parent folder.
    parent = os.path.dirname(root)
    try:
        for name in sorted(os.listdir(parent)):
            p = os.path.join(parent, name)
            if os.path.isdir(os.path.join(p, ".git")):
                repos.append(os.path.normpath(p))
    except OSError:
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
    """Return (ok, message or None)."""
    name = os.path.basename(repo)
    code, out = git(repo, "fetch", "-q", "origin")
    if code != 0:
        return True, f"{name}: fetch failed ({out.splitlines()[-1] if out else 'no output'})"
    base = default_branch(repo)
    if not base:
        return True, None
    code, behind = git(repo, "rev-list", "--count", f"HEAD..origin/{base}")
    if code != 0 or behind == "0":
        return True, None
    code, out = git(repo, "merge", "--no-edit", f"origin/{base}")
    if code == 0:
        return True, f"{name}: pulled {behind} new commit(s) from {base}"
    git(repo, "merge", "--abort")
    return False, (f"{name}: {base} has {behind} new commit(s) that conflict with "
                   f"local changes; merge aborted, nothing changed. Resolve before writing.")


def sync_all(cwd):
    ok, msgs = True, []
    for repo in find_repos(cwd):
        r_ok, msg = sync(repo)
        ok = ok and r_ok
        if msg:
            msgs.append(msg)
    return ok, msgs


def read_hook():
    try:
        return json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        return {}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "start"
    data = read_hook()
    cwd = data.get("cwd") or os.getcwd()
    cmd = (data.get("tool_input") or {}).get("command", "")

    if mode == "start":
        ok, msgs = sync_all(cwd)
        if msgs:
            print("Git sync: " + " | ".join(msgs))
        return 0

    if mode == "pre-tool":
        if "git commit" not in cmd and "git push" not in cmd:
            return 0
        ok, msgs = sync_all(cwd)
        if not ok:
            print("Git sync: " + " | ".join(msgs), file=sys.stderr)
            return 2
        if msgs:
            print("Git sync: " + " | ".join(msgs), file=sys.stderr)
        return 0

    if mode == "post-tool":
        if "git push" not in cmd:
            return 0
        repo = repo_root(cwd)
        if not repo:
            return 0
        git(repo, "fetch", "-q", "origin")
        code, out = git(repo, "status", "-sb")
        first = out.splitlines()[0] if out else ""
        if "behind" in first or "ahead" in first:
            print(f"Git sync: after push, {os.path.basename(repo)} still differs from origin: {first}",
                  file=sys.stderr)
            return 2
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
