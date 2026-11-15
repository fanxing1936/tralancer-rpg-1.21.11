"""HE/AV 最小增量安装：默认只出计划；明确 --apply PLAN 才写测试实例。

不复制整个包、不改pack.mcmeta、不删文件。共享JSON只合并本任务前缀与hooks。
apply重新生成计划并逐文件核对源/旧目标SHA；覆盖前备份，每步写receipt。
调用者仍须先取得用户的同步许可；此脚本本身不把计划视为用户许可。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "_tools/heart_of_ender_ref/build_validation"
VERSION = Path(r"D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3")
TARGETS = {"rp": VERSION / "resourcepacks/tralancer-rpg",
           "dp": VERSION / "saves/新的世界/datapacks/tralancer-rpg"}
KEYS = ("heart_of_ender", "arch_visage")
OWNER = "ender_debug_install.py/v1"
OWN_DIRS = {
    "rp": [f"assets/rpg/{kind}/{key}" for key in KEYS for kind in ("models", "items", "sounds")]
          + [f"assets/rpg/textures/item/{key}" for key in KEYS],
    "dp": [f"data/rpg/{kind}/{key}" for key in KEYS for kind in ("function", "predicate")],
}
SHARED = {"rp": {"assets/rpg/sounds.json": "sounds", "assets/rpg/lang/zh_cn.json": "lang",
                 "assets/rpg/lang/en_us.json": "lang"},
          "dp": {f"data/minecraft/tags/function/{kind}.json": kind for kind in ("load", "tick")}}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return path.read_bytes() if path.is_file() else None


def digest(data):
    return None if data is None else sha(data)


def safe_target(pack, relative):
    nominal = Path(os.path.abspath(TARGETS[pack]))
    base = nominal.resolve()
    if base != nominal or VERSION.resolve() not in base.parents:
        raise ValueError(f"测试实例包路径被重定向/越界：{nominal}")
    path = (base / relative).resolve()
    if base not in path.parents:
        raise ValueError(f"目标路径越界：{path}")
    allowed = relative in SHARED[pack] or any(relative.startswith(p + "/") for p in OWN_DIRS[pack])
    if not allowed or path.name == "pack.mcmeta":
        raise ValueError(f"不是本任务安装路径：{relative}")
    return path


def tag_id(value):
    return value if isinstance(value, str) else value.get("id")


def merge_shared(kind, old, source):
    target = json.loads(old) if old is not None else ({"values": []} if kind in ("load", "tick") else {})
    source = json.loads(source)
    if kind in ("sounds", "lang"):
        prefixes = tuple(("subtitles.rpg." if kind == "lang" else "") + key + "." for key in KEYS)
        entries = {key: value for key, value in source.items() if key.startswith(prefixes)}
        if not all(any(k.startswith(prefix) for k in entries) for prefix in prefixes):
            raise ValueError(f"源{kind}缺少HE或AV条目")
        # 不删除任何未知/旧条目；本任务相同键按已构建源更新。
        target.update(entries)
        return target
    own = [f"rpg:{key}/{kind}" for key in KEYS]
    if kind == "tick":
        own += [f"rpg:{key}/tick_late" for key in KEYS]
    if not set(own).issubset({tag_id(v) for v in source["values"]}):
        raise ValueError(f"源{kind}标签缺少本任务hook")
    values = target.setdefault("values", [])
    # 只去重/重排自己hook；其它条目、顺序及replace等顶层字段全部保留。
    values[:] = [v for v in values if tag_id(v) not in own]
    if kind == "load":
        values.extend(own)
    else:
        ids = [tag_id(v) for v in values]
        index = ids.index("rpg:command/tick_end") if "rpg:command/tick_end" in ids else len(values)
        values[index:index] = [f"rpg:{key}/tick" for key in KEYS]
        values.extend(f"rpg:{key}/tick_late" for key in KEYS)
    return target


def plan(source_rp, source_dp):
    sources = {"rp": Path(source_rp).resolve(strict=True), "dp": Path(source_dp).resolve(strict=True)}
    inventory, targets, operations = {}, {}, []
    for pack in ("dp", "rp"):
        source = sources[pack]
        paths = {}
        for relative in OWN_DIRS[pack]:
            directory = source / relative
            if not directory.is_dir():
                raise ValueError(f"源模型目录尚未构建：{directory}")
            for file in directory.rglob("*"):
                if file.is_file():
                    resolved = file.resolve()
                    if source not in resolved.parents:
                        raise ValueError(f"源目录含越界链接：{file}")
                    paths[file.relative_to(source).as_posix()] = "copy"
        paths.update(SHARED[pack])
        for relative, kind in sorted(paths.items()):
            src = source / relative
            src_data = src.read_bytes()
            target = safe_target(pack, relative)
            old = read(target)
            content = src_data if kind == "copy" else encode(merge_shared(kind, old, src_data))
            identity = pack + "/" + relative
            inventory[identity] = sha(src_data)
            targets[identity] = digest(old)
            if old == content:
                continue
            row = {"pack": pack, "relative_path": relative, "source": str(src), "target": str(target),
                   "mode": kind, "source_sha256": sha(src_data), "old_sha256": digest(old),
                   "new_sha256": sha(content), "new_bytes": len(content),
                   "change": "add" if old is None else "replace", "backup_required": old is not None}
            if kind != "copy":
                row["merged_json"] = json.loads(content)
            operations.append(row)
    return {"owner": OWNER, "source_roots": {k: str(v) for k, v in sources.items()},
            "target_roots": {k: str(v.resolve()) for k, v in TARGETS.items()},
            "source_inventory": inventory, "target_inventory": targets, "operations": operations,
            "summary": {"files_to_write": len(operations), "add": sum(x["change"] == "add" for x in operations),
                        "replace": sum(x["change"] == "replace" for x in operations),
                        "unchanged": len(inventory) - len(operations), "delete": 0,
                        "bytes_to_write": sum(x["new_bytes"] for x in operations)},
            "backup_plan": {"root": str(ARTIFACTS / "install_backup"),
                            "layout": "UTCtimestamp_planSHA8/{dp|rp}/relative_path", "copies": sum(x["backup_required"] for x in operations)},
            "preserved": ["pack.mcmeta", "所有非HE/AV文件与命名空间", "所有未知路径（不删除）",
                          "共享标签的其它条目与顺序", "sounds/lang的其它前缀"],
            "permission": "Plan only. User approval to synchronize is required before --apply."}


def write_artifact(path, value):
    path = path.resolve()
    if ARTIFACTS.resolve() not in path.parents:
        raise ValueError("计划/receipt必须位于本任务build_validation目录")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def apply(plan_path):
    raw_plan = plan_path.read_bytes()
    approved = json.loads(raw_plan)
    if approved.get("owner") != OWNER:
        raise ValueError("不是本脚本的计划")
    current = plan(approved["source_roots"]["rp"], approved["source_roots"]["dp"])
    if current != approved:
        raise ValueError("计划之后源文件/目标文件/范围已变；拒绝同步，请重新生成计划并审阅")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup = ARTIFACTS / "install_backup" / (stamp + "_" + sha(raw_plan)[:8])
    receipt_path = ARTIFACTS / "install_receipts" / (stamp + ".json")
    receipt = {"owner": OWNER, "plan": str(plan_path.resolve()), "plan_sha256": sha(raw_plan),
               "backup_root": str(backup), "target_roots": approved["target_roots"],
               "status": "running", "written": [], "summary": approved["summary"]}
    write_artifact(receipt_path, receipt)
    try:
        for row in approved["operations"]:
            target = safe_target(row["pack"], row["relative_path"])
            old = read(target)
            if digest(old) != row["old_sha256"]:
                raise ValueError(f"写入前目标被改动：{target}")
            src_data = Path(row["source"]).read_bytes()
            if sha(src_data) != row["source_sha256"]:
                raise ValueError(f"写入前源被改动：{row['source']}")
            data = src_data if row["mode"] == "copy" else encode(merge_shared(row["mode"], old, src_data))
            if sha(data) != row["new_sha256"]:
                raise ValueError("实际合并结果不等于已审阅计划")
            saved = None
            if old is not None:
                saved = backup / row["pack"] / row["relative_path"]
                if backup.resolve() not in saved.resolve().parents:
                    raise ValueError("备份路径越界")
                saved.parent.mkdir(parents=True, exist_ok=True)
                with saved.open("xb") as stream:
                    stream.write(old)
            target.parent.mkdir(parents=True, exist_ok=True)
            if old is None:
                with target.open("xb") as stream:
                    stream.write(data)
            else:
                temporary = target.with_name(target.name + ".he_av_install_tmp")
                with temporary.open("xb") as stream:
                    stream.write(data)
                if digest(read(target)) != row["old_sha256"]:
                    temporary.unlink()  # 仅删除刚由本调用独占创建的临时文件。
                    raise ValueError(f"原子替换前目标被改动：{target}")
                os.replace(temporary, target)
            if sha(target.read_bytes()) != row["new_sha256"]:
                raise IOError(f"写后SHA不一致：{target}")
            receipt["written"].append({"target": str(target), "sha256": row["new_sha256"], "backup": str(saved) if saved else None})
            write_artifact(receipt_path, receipt)
        receipt["status"] = "complete"
    except Exception as error:
        receipt["status"] = "partial_failure"
        receipt["error"] = str(error)
        write_artifact(receipt_path, receipt)
        raise
    write_artifact(receipt_path, receipt)
    return receipt_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="仅计划（默认）")
    mode.add_argument("--apply", type=Path, metavar="PLAN", help="必须已经取得用户同步许可")
    parser.add_argument("--source-rp", type=Path, default=ROOT / "resourcepack")
    parser.add_argument("--source-dp", type=Path, default=ROOT / "rpg")
    parser.add_argument("--out", type=Path, default=ARTIFACTS / "install_plan.json")
    args = parser.parse_args()
    if args.apply:
        print(apply(args.apply))
    else:
        record = plan(args.source_rp, args.source_dp)
        write_artifact(args.out, record)
        print(json.dumps({"plan": str(args.out.resolve()), **record["summary"], "applied": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
