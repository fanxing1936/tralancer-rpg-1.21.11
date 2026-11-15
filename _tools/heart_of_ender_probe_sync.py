"""仅扩展已获授权的 he_material_probe 测试包；不操作游戏或正式 RPG 包。"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from heart_of_ender_blockbench import REF

STAGE = REF / 'm3_material_v3'
SOURCE = STAGE / 'motion_probe'
INSTANCE = Path(r'D:\minecraft\PCL启动器\.minecraft\versions\1.21.11-Fabric 0.19.3')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text('utf8'))


def sync(apply=False):
    receipt_path = STAGE / 'motion_probe_sync_receipt.json'
    previous_path = receipt_path if receipt_path.exists() else STAGE / 'sync_receipt.json'
    previous = read(previous_path)
    if previous.get('user_authorized') is not True:
        raise RuntimeError('未找到用户已授权的独立测试包同步记录')
    generated = read(SOURCE / 'GENERATED_FILES.json')['files']
    manifest = read(SOURCE / 'motion_probe_manifest.json')
    current_sha = sha((REF / 'heart_of_ender.bbmodel').read_bytes())
    if manifest['model_sha256'] != current_sha:
        raise RuntimeError('动作包不对应当前模型，请先重建与复核')
    roots = {'resourcepack': (INSTANCE / 'resourcepacks/he_material_probe').resolve(),
             'datapack': (INSTANCE / 'saves/新的世界/datapacks/he_material_probe').resolve()}
    prior = {Path(f['destination']).resolve(): f['sha256'] for f in previous['files']}
    planned = {}
    for relative, checksum in generated.items():
        rel = Path(relative)
        if rel.parts[0] not in roots:
            continue
        source = (SOURCE / rel).resolve()
        root = roots[rel.parts[0]]
        destination = (root / Path(*rel.parts[1:])).resolve()
        if SOURCE.resolve() not in source.parents or root not in destination.parents:
            raise RuntimeError(f'越界路径：{relative}')
        data = source.read_bytes()
        if sha(data) != checksum:
            raise RuntimeError(f'生成文件被修改：{source}')
        planned[destination] = (data, checksum)
    if not set(prior).issubset(planned):
        raise RuntimeError('新探针删除了原有文件，需显式迁移；本工具不执行删除')
    for destination, checksum in prior.items():
        if not any(r in destination.parents for r in roots.values()):
            raise RuntimeError('旧收据目标越界')
        if not destination.is_file() or sha(destination.read_bytes()) != checksum:
            raise RuntimeError(f'实例中存在用户/其它会话修改，停止覆盖：{destination}')
    for destination in set(planned) - set(prior):
        if destination.exists():
            raise RuntimeError(f'新增路径已有未知文件，停止覆盖：{destination}')
    additions = len(set(planned) - set(prior))
    replacements = sum(p in prior and prior[p] != c for p, (_, c) in planned.items())
    result = {'applied': apply, 'files_verified': len(planned), 'new_files': additions,
              'updated_files': replacements, 'model_sha256': current_sha}
    if apply:
        for destination, (data, checksum) in planned.items():
            if prior.get(destination) == checksum:
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        if not all(sha(p.read_bytes()) == c for p, (_, c) in planned.items()):
            raise RuntimeError('同步后哈希检查失败')
        receipt = {'user_authorized': True, 'scope': previous['scope'],
                   'authorization': '继续原已授权的独立 he_material_probe 同步；本轮用户要求继续M3收尾',
                   'previous_receipt': str(previous_path),
                   'previous_receipt_sha256': sha(previous_path.read_bytes()),
                   'synced_at_utc': datetime.now(timezone.utc).isoformat(),
                   'model_sha256': current_sha, 'source_manifest_sha256': sha((SOURCE / 'GENERATED_FILES.json').read_bytes()),
                   'files': [{'destination': str(p), 'sha256': c} for p, (_, c) in sorted(planned.items())],
                   'changes': result, 'game_reload_performed': False,
                   'reload': '用户执行 /reload 并按 F3+T；本工具不操作游戏界面'}
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', 'utf8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='默认只检查；通过本轮测试后才应用')
    args = parser.parse_args()
    sync(args.apply)
