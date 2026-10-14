"""Rebuild every index in a project's .brain/ folder.

    python ~/.claude/skills/brain/brain_index.py [path]     # path: anywhere inside the project (default: here)
    python ~/.claude/skills/brain/brain_index.py --hook     # called by Claude Code hooks; reads the hook JSON on stdin

Builds thoughts/, ideas/, plans/, design/, knowledge/ and tools/ index.md from
the files' own content (the format is in SKILL.md next to this script), and
rewrites the "Open right now" part of the main .brain/index.md. At the end of a
reply (the Stop hook) it also rebuilds the brains in sibling folders, for VS Code
workspaces with several projects. Files are only
written when their content changes. Does nothing if there is no .brain/.
"""
import ast
import json
import pathlib
import re
import sys

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
AUTO = "<!-- auto: everything below is rebuilt by brain_index.py -->"
FOLDERS = {
    "thoughts": "Questions and random thoughts I have while working. They can lead to ideas.",
    "ideas": "What I could do, grouped by status. No status = still just an idea; then planned, done or dropped.",
    "plans": "What I'll do. One file per plan, with how many steps are left.",
    "design": "What it is: every design decision, with the date and why.",
    "knowledge": "Research results, with the date checked and the source.",
    "tools": "Claude's helper scripts for this project, from each script's own description.",
    "modes": "What only one mode needs (tutor's re-quiz list, coach's learning record), one file per mode.",
}
HEADER = "*{} Built by `brain_index.py`; don't edit by hand.*"


def find_brain(start):
    p = pathlib.Path(start).resolve()
    for d in [p, *p.parents]:
        if (d / ".brain").is_dir():
            return d / ".brain"
    return None


def write(path, text):
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")


def notes(folder):
    return sorted(p for p in folder.glob("*.md") if p.name != "index.md")


def title_and_summary(text, fallback):
    title, summary = fallback, ""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# ") and title == fallback:
            title = s[2:].strip()
        elif s.startswith("*") and s.endswith("*") and len(s) > 2 and not summary:
            summary = s.strip("*").strip()
            break
        elif s.startswith("## "):
            break
    return title, summary


def entry(p, text, extra=""):
    title, summary = title_and_summary(text, p.stem)
    line = f"- [{p.name}]({p.name}): **{title}**"
    if summary:
        line += f". {summary}"
    return line + (f" ({extra})" if extra else "")


def dated(text):
    """'3 entries, newest 2026-10-14' from ## headings and dates in the file."""
    n = len(re.findall(r"^## ", text, flags=re.M))
    dates = DATE.findall(text)
    bits = [f"{n} entr{'y' if n == 1 else 'ies'}"] if n else []
    if dates:
        bits.append(f"newest {max(dates)}")
    return ", ".join(bits)


def issues(text):
    """'2 known issues' from a '## Known issues' section."""
    m = re.search(r"^## Known issues\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    n = len(re.findall(r"^- ", m.group(1), flags=re.M)) if m else 0
    return f"{n} known issue{'s' if n != 1 else ''}" if n else ""


def ideas(folder):
    """Every idea (## heading) with its status line, grouped by the latest status."""
    groups = {"open": [], "planned": [], "done": [], "dropped": []}
    for p in notes(folder):
        for block in re.split(r"^## ", p.read_text(encoding="utf-8"), flags=re.M)[1:]:
            name = block.splitlines()[0].strip()
            m = re.search(r"^- \*\*Status:\*\*\s*(.+)$", block, flags=re.M)
            status = m.group(1).strip() if m else ""
            last = status.split("→")[-1].strip().lower() if status else ""
            word = next((w for w in ("planned", "done", "dropped") if last.startswith(w)), None)
            if word is None and status:  # history like "planned 10-13 → plans/x.md": find the last status word
                found = re.findall(r"\b(planned|done|dropped)\b", status.lower())
                word = found[-1] if found else "open"
            groups[word or "open"].append(f"- **{name}** ([{p.name}]({p.name}))" + (f": {status}" if status else ""))
    out = []
    for key, label in [("open", "Open (still just ideas)"), ("planned", "Planned"), ("done", "Done"), ("dropped", "Dropped")]:
        out += [f"## {label}", ""] + (groups[key] or ["- none"]) + [""]
    return out, groups


def field(text, name):
    m = re.search(rf"^- \*\*{name}:\*\*\s*(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else ""


def plans(folder):
    lines, open_plans = [], []
    for p in notes(folder):
        text = p.read_text(encoding="utf-8")
        todo = len(re.findall(r"^\s*- \[ \]", text, flags=re.M))
        done = len(re.findall(r"^\s*- \[[xX]\]", text, flags=re.M))
        held = len(re.findall(r"^\s*- \[ \] \(on hold\)", text, flags=re.M))
        steps = f"{todo} of {todo + done} steps left" if todo + done else "no steps yet"
        if held:
            steps += f", {held} on hold"
        nxt = field(text, "Next step")
        lines.append(entry(p, text, steps) + (f"\n  - Next step: {nxt}" if nxt else ""))
        title, summary = title_and_summary(text, p.stem)
        if todo > held or not todo + done:
            open_plans.append(f"- [{title}](plans/{p.name}): " + (f"next: {nxt}" if nxt else steps))
    return lines, open_plans


def tools(folder):
    lines = []
    for p in sorted(folder.glob("*")):
        if p.suffix not in (".py", ".ps1", ".js", ".sh"):
            continue
        text = p.read_text(encoding="utf-8")
        doc = ""
        if p.suffix == ".py":
            try:
                doc = ast.get_docstring(ast.parse(text)) or ""
            except SyntaxError:
                pass
        else:
            doc = "\n".join(l.lstrip("#/ ").rstrip() for l in text.splitlines()[:15] if l.startswith(("#", "//")))
        lines += [f"## `{p.name}`", "", doc.strip() or "(no description yet)", ""]
    return lines


def build(brain):
    open_plans, open_ideas = [], []
    for name, blurb in FOLDERS.items():
        folder = brain / name
        if not folder.is_dir():
            continue
        out = [f"# {name.capitalize()}", "", HEADER.format(blurb), ""]
        if name == "ideas":
            body, groups = ideas(folder)
            out += body
            open_ideas = [re.sub(r"\]\(([^)/]+\.md)\)", r"](ideas/\1)", l) for l in groups["open"]]
        elif name == "plans":
            body, open_plans = plans(folder)
            out += body + [""]
        elif name == "tools":
            out += tools(folder)
        elif name == "design":
            out += [entry(p, t, ", ".join(x for x in [dated(t), issues(t)] if x)) for p in notes(folder) for t in [p.read_text(encoding="utf-8")]] + [""]
        else:
            out += [entry(p, t, dated(t)) for p in notes(folder) for t in [p.read_text(encoding="utf-8")]] + [""]
        write(folder / "index.md", "\n".join(out).rstrip() + "\n")

    main = brain / "index.md"
    head = main.read_text(encoding="utf-8").split(AUTO)[0].rstrip() if main.exists() else "# Brain index"
    auto = [AUTO, "", "## Open right now", "", "**Plans with steps left:**"] + (open_plans or ["- none"])
    auto += ["", "**Ideas not decided yet:**"] + (open_ideas or ["- none"])
    write(main, head + "\n\n" + "\n".join(auto) + "\n")


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        try:
            data = json.load(sys.stdin)
        except ValueError:
            return
        path = (data.get("tool_input") or {}).get("file_path")
        if path and ".brain" not in pathlib.Path(path).parts:
            return  # a Write/Edit outside .brain/: nothing to rebuild
        start = pathlib.Path(path).parent if path else data.get("cwd", ".")
        if not path:  # end of a reply: also rebuild the brains next to this project (other workspace folders)
            brain = find_brain(start)
            root = brain.parent if brain else pathlib.Path(start).resolve()
            for sibling in root.parent.iterdir():
                if sibling != root and (sibling / ".brain").is_dir():
                    build(sibling / ".brain")
    else:
        start = args[0] if args else "."
    brain = find_brain(start)
    if brain:
        build(brain)
        if "--hook" not in args:
            print(f"rebuilt indexes in {brain}")


if __name__ == "__main__":
    main()
