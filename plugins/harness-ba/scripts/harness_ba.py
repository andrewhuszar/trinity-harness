"""harness-ba: tervezési tér bootstrap és a következő teendő meghatározása.

Használat:
  harness_ba.py init --prefix PRT --project "Prototípus" [--linked-repo URL]
  harness_ba.py next
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_core as core  # noqa: E402

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_ROOT = os.path.join(PLUGIN_ROOT, "templates", "planning")
ROLE = "planning"

EPIC_STATES = ["Vázlat", "Pontosítva", "Tervezés alatt", "Bontva", "Fejlesztés alatt", "Kiadva", "Lezárva", "Jegelve"]
STORY_STATES = ["Fejlesztésre kész", "Fejlesztés alatt", "Tesztelés alatt", "Elfogadva", "Kiadva", "Jegelve"]

# Prioritás szerint: a lista elején álló teendő a sürgősebb.
EPIC_ACTIONS = {
    "Vázlat": (2, "Pontosítás folytatása", "Az epic üzleti igénye és folyamatmodellje még nincs elfogadva."),
    "Pontosítva": (3, "Funkcionális specifikáció indítása", "Az epic pontosítva, a tervezési sávok még nem indultak el."),
    "Tervezés alatt": (4, "Funkcionális specifikáció és design lezárása, majd bontás", "Az epic tervezés alatt áll."),
}


def init(args):
    root = os.getcwd()
    plugin = core.plugin_info(PLUGIN_ROOT)
    try:
        config = core.new_config(ROLE, args.prefix, args.project, plugin, args.linked_repo)
        config_file = core.write_config(root, config)
    except FileExistsError as error:
        core.emit({"ok": False, "error": "A harness-konfiguráció már létezik; a bootstrap nem írja felül.", "path": str(error)}, 1)
    except ValueError as error:
        core.emit({"ok": False, "error": str(error)}, 1)
    created, skipped = [os.path.relpath(config_file, root)], []
    core.copy_template(TEMPLATE_ROOT, root, {"<PREFIX>": args.prefix, "<PROJEKT>": args.project}, created, skipped)
    core.emit({"ok": True, "plugin": plugin, "created": created, "skipped": skipped})


def next_action(_args):
    root = os.getcwd()
    plugin = core.plugin_info(PLUGIN_ROOT)
    config = core.load_config(root)
    if config is None:
        core.emit({"plugin": plugin, "next": {
            "action": "A tervezési tér bootstrapolása",
            "reason": "Ebben a repóban nincs harness-konfiguráció.",
            "command": "/harness-ba:init",
        }})
    if config.get("role") != ROLE:
        core.emit({"plugin": plugin, "next": {
            "action": "A harness-dev plugin használata",
            "reason": f"Ez a repó szerepe '{config.get('role')}', nem tervezési tér.",
            "command": "/harness-dev:next",
        }})

    todos, warnings, blocked = [], [], []

    def collect_blocked(meta, target):
        if meta.get("blocked_reason"):
            blocked.append({"target": target, "reason": meta["blocked_reason"], "owner": meta.get("blocked_owner"), "until": meta.get("blocked_until")})

    domains = [d for d in core.subdirectories(os.path.join(root, "domains")) if os.path.exists(os.path.join(root, "domains", d, "context.md"))]
    if not domains:
        todos.append((1, {
            "action": "Az első domain felvétele",
            "reason": "A tervezési térben még nincs domain; az epicek a domain szótárára és határaira épülnek.",
            "target": "domains/<domain>/context.md",
        }))

    epics = core.subdirectories(os.path.join(root, "epics"))
    for epic in epics:
        meta = core.front_matter(os.path.join(root, "epics", epic, "epic.md"))
        status = meta.get("status")
        collect_blocked(meta, f"epics/{epic}")
        if status not in EPIC_STATES:
            warnings.append(f"epics/{epic}/epic.md: ismeretlen vagy hiányzó állapot ({status!r}).")
            continue
        if status in EPIC_ACTIONS:
            priority, action, reason = EPIC_ACTIONS[status]
            todos.append((priority, {"action": action, "reason": reason, "target": f"epics/{epic}"}))
        stories_dir = os.path.join(root, "epics", epic, "stories")
        if os.path.isdir(stories_dir):
            for name in sorted(os.listdir(stories_dir)):
                if not name.endswith(".md"):
                    continue
                story_meta = core.front_matter(os.path.join(stories_dir, name))
                story_status = story_meta.get("status")
                collect_blocked(story_meta, f"epics/{epic}/stories/{name}")
                if story_status not in STORY_STATES:
                    warnings.append(f"epics/{epic}/stories/{name}: ismeretlen vagy hiányzó állapot ({story_status!r}).")
                elif story_status == "Tesztelés alatt":
                    todos.append((0, {
                        "action": "Story elfogadása a tesztkörnyezetben",
                        "reason": "A story tesztelés alatt áll, és BA-elfogadásra vár.",
                        "target": f"epics/{epic}/stories/{name}",
                    }))

    if domains and not epics:
        todos.append((5, {
            "action": "Az első epic felvétele rövid üzleti leírásból",
            "reason": "Van domain, de még nincs epic.",
            "target": "epics/<EPIC-ID>/epic.md",
        }))

    todos.sort(key=lambda item: item[0])
    result = {"plugin": plugin, "project": config.get("project"), "warnings": warnings, "blocked": blocked}
    if todos:
        result["next"] = todos[0][1]
        result["other"] = [item[1] for item in todos[1:]]
    else:
        result["next"] = {"action": "Nincs BA-teendő", "reason": "Minden epic fejlesztés alatt, kiadva, lezárva vagy jegelve."}
    core.emit(result)


def main():
    parser = argparse.ArgumentParser(prog="harness_ba")
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init")
    init_parser.add_argument("--prefix", required=True)
    init_parser.add_argument("--project", required=True)
    init_parser.add_argument("--linked-repo")
    init_parser.set_defaults(handler=init)
    next_parser = commands.add_parser("next")
    next_parser.set_defaults(handler=next_action)
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
