"""A harness-pluginok közös segédfüggvényei.

A forrás a `shared/harness_core.py`; a pluginokba a `scripts/sync-shared.sh` másolja.
Csak a Python standard könyvtárát használja.
"""

import json
import os
import re
import sys

CONFIG_DIR = ".harness"
CONFIG_FILE = "config.json"
SCHEMA_VERSION = 1
STRUCTURE_VERSION = 1
PREFIX_PATTERN = re.compile(r"^[A-Z][A-Z0-9]{1,9}$")


def config_path(root):
    return os.path.join(root, CONFIG_DIR, CONFIG_FILE)


def load_config(root):
    path = config_path(root)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def write_config(root, config):
    """Új konfigurációt ír; meglévőt soha nem ír felül."""
    path = config_path(root)
    if os.path.exists(path):
        raise FileExistsError(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def plugin_info(plugin_root):
    with open(os.path.join(plugin_root, ".claude-plugin", "plugin.json"), encoding="utf-8") as handle:
        manifest = json.load(handle)
    return {"name": manifest["name"], "version": manifest.get("version", "ismeretlen")}


def new_config(role, prefix, project, plugin, linked_repo=None, workflow="harness"):
    if not PREFIX_PATTERN.match(prefix):
        raise ValueError("A story-prefix 2–10 karakter, nagybetűvel kezdődik, és csak nagybetűt vagy számjegyet tartalmaz.")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "structureVersion": STRUCTURE_VERSION,
        "role": role,
        "project": project,
        "storyPrefix": prefix,
        "linkedRepo": linked_repo,
        "workflow": workflow,
        "createdWith": plugin,
    }


def write_new_file(root, relative_path, content, created, skipped):
    """Létrehoz egy fájlt, ha még nem létezik; a meglévőt érintetlenül hagyja."""
    path = os.path.join(root, relative_path)
    if os.path.exists(path):
        skipped.append(relative_path)
        return
    os.makedirs(os.path.dirname(path) or root, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    created.append(relative_path)


def copy_template(template_root, root, replacements, created, skipped, exclude=()):
    for directory, _, files in os.walk(template_root):
        for name in sorted(files):
            source = os.path.join(directory, name)
            relative = os.path.relpath(source, template_root)
            if relative in exclude:
                continue
            with open(source, encoding="utf-8") as handle:
                content = handle.read()
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            write_new_file(root, relative, content, created, skipped)


def front_matter(path):
    """Egy markdown-fájl `---` közötti `kulcs: érték` sorait adja vissza."""
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return result
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def subdirectories(path):
    if not os.path.isdir(path):
        return []
    return sorted(name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) and not name.startswith("."))


def emit(payload, exit_code=0):
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    sys.exit(exit_code)
