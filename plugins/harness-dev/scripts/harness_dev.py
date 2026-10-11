"""harness-dev: termékrepó bootstrap és a következő teendő meghatározása.

Használat:
  harness_dev.py init --prefix PRT --project "Prototípus" [--linked-repo URL] [--workflow harness|quick-start]
  harness_dev.py next
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_core as core  # noqa: E402

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = {
    "harness": os.path.join(PLUGIN_ROOT, "templates", "product"),
    "quick-start": os.path.join(PLUGIN_ROOT, "templates", "quick-start"),
}
ROLE = "product"
STORY_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")


def init(args):
    root = os.getcwd()
    plugin = core.plugin_info(PLUGIN_ROOT)
    try:
        config = core.new_config(ROLE, args.prefix, args.project, plugin, args.linked_repo, args.workflow)
        config_file = core.write_config(root, config)
    except FileExistsError as error:
        core.emit({"ok": False, "error": "A harness-konfiguráció már létezik; a bootstrap nem írja felül.", "path": str(error)}, 1)
    except ValueError as error:
        core.emit({"ok": False, "error": str(error)}, 1)
    created, skipped = [os.path.relpath(config_file, root)], []
    # A gyorsindító sablon README-je a sablon használatát írja le, a projektbe nem kerül.
    core.copy_template(TEMPLATES[args.workflow], root, {"<PREFIX>": args.prefix, "<PROJEKT>": args.project}, created, skipped, exclude=("README.md",))
    core.emit({"ok": True, "plugin": plugin, "workflow": args.workflow, "created": created, "skipped": skipped})


def quick_start_todos(root):
    index = os.path.join(root, "plan", "stories", "README.md")
    rows = []
    if os.path.exists(index):
        with open(index, encoding="utf-8") as handle:
            for line in handle:
                match = STORY_ROW.match(line.strip())
                if match:
                    rows.append({"id": match.group(1), "title": match.group(2), "status": match.group(3)})
    todos = []
    for row in rows:
        if row["status"] == "Folyamatban":
            todos.append((0, {"action": f"{row['id']} folytatása", "reason": "A story folyamatban van.", "target": row["id"]}))
        elif row["status"] == "Tervezve":
            todos.append((1, {"action": f"{row['id']} indítása", "reason": "A story tervezett, és nincs előtte folyamatban lévő munka.", "target": row["id"]}))
    if not rows:
        todos.append((2, {"action": "Az első story megírása", "reason": "A story-index üres.", "target": "plan/stories/_story-sablon.md"}))
    return todos, []


def harness_todos(root):
    todos, warnings = [], []
    epics_dir = os.path.join(root, "planning", "epics")
    epics = core.subdirectories(epics_dir)
    if not epics:
        todos.append((3, {
            "action": "Várakozás az első tervezési szinkronra",
            "reason": "A `planning/` még nem tartalmaz epicet; a tervezési térből a tervezési szinkron hozza.",
            "target": "planning/",
        }))
    for epic in epics:
        status = core.front_matter(os.path.join(epics_dir, epic, "epic.md")).get("status")
        spec = os.path.join(root, "docs", "epics", epic, "technikai-specifikacio.md")
        if status == "Tervezés alatt" and not os.path.exists(spec):
            todos.append((1, {
                "action": "Technikai specifikáció készítése",
                "reason": "Az epic tervezés alatt áll, és nincs technikai specifikációja.",
                "target": f"docs/epics/{epic}/technikai-specifikacio.md",
            }))
        stories_dir = os.path.join(epics_dir, epic, "stories")
        if not os.path.isdir(stories_dir):
            continue
        for name in sorted(os.listdir(stories_dir)):
            if not name.endswith(".md"):
                continue
            story_status = core.front_matter(os.path.join(stories_dir, name)).get("status")
            if story_status == "Fejlesztés alatt":
                todos.append((0, {"action": "Folyamatban lévő story folytatása", "reason": "A story fejlesztés alatt áll.", "target": f"planning/epics/{epic}/stories/{name}"}))
            elif story_status == "Fejlesztésre kész":
                todos.append((2, {"action": "Story fejlesztésének indítása", "reason": "A story fejlesztésre kész.", "target": f"planning/epics/{epic}/stories/{name}"}))
    return todos, warnings


def next_action(_args):
    root = os.getcwd()
    plugin = core.plugin_info(PLUGIN_ROOT)
    config = core.load_config(root)
    if config is None:
        core.emit({"plugin": plugin, "next": {
            "action": "A termékrepó bootstrapolása",
            "reason": "Ebben a repóban nincs harness-konfiguráció.",
            "command": "/harness-dev:init",
        }})
    if config.get("role") != ROLE:
        core.emit({"plugin": plugin, "next": {
            "action": "A harness-ba plugin használata",
            "reason": f"Ez a repó szerepe '{config.get('role')}', nem termékrepó.",
            "command": "/harness-ba:next",
        }})
    workflow = config.get("workflow", "harness")
    todos, warnings = quick_start_todos(root) if workflow == "quick-start" else harness_todos(root)
    todos.sort(key=lambda item: item[0])
    result = {"plugin": plugin, "project": config.get("project"), "workflow": workflow, "warnings": warnings}
    if todos:
        result["next"] = todos[0][1]
        result["other"] = [item[1] for item in todos[1:]]
    else:
        result["next"] = {"action": "Nincs fejlesztői teendő", "reason": "Nincs folyamatban lévő vagy indítható munka."}
    core.emit(result)


def main():
    parser = argparse.ArgumentParser(prog="harness_dev")
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init")
    init_parser.add_argument("--prefix", required=True)
    init_parser.add_argument("--project", required=True)
    init_parser.add_argument("--linked-repo")
    init_parser.add_argument("--workflow", choices=sorted(TEMPLATES), default="harness")
    init_parser.set_defaults(handler=init)
    next_parser = commands.add_parser("next")
    next_parser.set_defaults(handler=next_action)
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
