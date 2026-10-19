"""Pull the latest master into Rain's open repos when a chat starts (hook script).

What it does: for each repo it covers, fetches origin and merges the default
branch (master or main) into the current branch. A merge that would conflict
is aborted, never forced, and reported.

Which repos: the repo of the current folder, the folders listed in its
*.code-workspace file, and ~/.claude (dot-claude). In cloud sessions, also
every repo of mine next to the current one (where attached repos are cloned).

Cloud sessions also reset the local master to GitHub's: the container keeps
a frozen copy of master from when the environment was first set up.

How to run (the SessionStart hook calls it; reads hook JSON on stdin):
  python git_sync.py
"""
import json
import os
import subprocess
import sys

OWNER = "serina-sketch"
CLOUD = os.environ.get("CLAUDE_CODE_REMOTE") == "true"


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
    # Cloud: repos sit side by side (/home/user/<repo>), and the chat may
    # open in that parent folder rather than inside a repo.
    if CLOUD:
        parent = os.path.dirname(here) if here else os.path.abspath(cwd)
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


def fix_stale_base(repo, base):
    """Cloud: point the local base branch at GitHub's when it isn't checked out."""
    if git(repo, "rev-parse", "--verify", "-q", base)[0] != 0:
        return None
    if git(repo, "symbolic-ref", "-q", "--short", "HEAD")[1] == base:
        return None
    if git(repo, "rev-parse", base)[1] == git(repo, "rev-parse", f"origin/{base}")[1]:
        return None
    code, _ = git(repo, "branch", "-f", base, f"origin/{base}")
    return f"reset stale local {base} to GitHub's" if code == 0 else None


def sync(repo):
    """Return a message, or None when there was nothing to do."""
    name = os.path.basename(repo)
    code, out = git(repo, "fetch", "-q", "origin")
    if code != 0:
        return f"{name}: fetch failed ({out.splitlines()[-1] if out else 'no output'})"
    base = default_branch(repo)
    if not base:
        return None
    reset = fix_stale_base(repo, base) if CLOUD else None
    code, behind = git(repo, "rev-list", "--count", f"HEAD..origin/{base}")
    if code != 0 or behind == "0":
        return f"{name}: {reset}" if reset else None
    code, out = git(repo, "merge", "--no-edit", f"origin/{base}")
    if code == 0:
        return f"{name}: pulled {behind} new commit(s) from {base}" + (f", {reset}" if reset else "")
    git(repo, "merge", "--abort")
    return (f"{name}: {base} has {behind} new commit(s) that conflict with "
            f"local changes; merge aborted, nothing changed. Resolve before writing.")


def main():
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    repos = find_repos(cwd)
    msgs = [m for m in (sync(r) for r in repos) if m]
    # Always print a line, so a quiet run can be told apart from no run.
    if msgs:
        print("Git sync: " + " | ".join(msgs))
    else:
        print(f"Git sync: {len(repos)} repo(s) up to date "
              f"({', '.join(os.path.basename(r) or r for r in repos)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
