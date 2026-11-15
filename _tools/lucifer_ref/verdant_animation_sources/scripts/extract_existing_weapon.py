"""Repeat the headless call into existing Minecraft client classes. Scratch writes only."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

WORK=Path(__file__).resolve().parent
GAME=Path(r'D:\minecraft\PCL启动器\.minecraft')
VERSION=GAME/'versions/1.21.11-Fabric 0.19.3/1.21.11-Fabric 0.19.3.json'
JAR=VERSION.with_suffix('.jar')
PNG=Path(r'D:\agent\claude\github-create\tralancer-rpg-1.21.11\resourcepack\assets\rpg\textures\item\lucifer_in_hand.png')
doc=json.loads(VERSION.read_text(encoding='utf-8'))
assert hashlib.sha1(JAR.read_bytes()).hexdigest()=='ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd', 'Mapped class names are specific to this 1.21.11 client'
assert not PNG.with_suffix('.png.mcmeta').exists(), 'This extractor provides the single static frame used by the current sprite'
classes=WORK/'client_classes_readonly_copy';classes.mkdir(exist_ok=True)
with zipfile.ZipFile(JAR) as z:
    for name in z.namelist():
        if '/' not in name and name.endswith('.class'):
            path=classes/name
            data=z.read(name)
            if not path.exists() or path.read_bytes()!=data: path.write_bytes(data)
    (WORK/'spear_in_hand.original.json').write_bytes(z.read('assets/minecraft/models/item/spear_in_hand.json'))
cp=[str(WORK),str(classes),str(JAR)]
for lib in doc['libraries']:
    path=lib.get('downloads',{}).get('artifact',{}).get('path')
    if path and (GAME/'libraries'/path).is_file(): cp.append(str(GAME/'libraries'/path))
classpath=';'.join(cp)
(WORK/'weapon_classpath.txt').write_text(classpath,encoding='utf-8')
subprocess.run(['javac','-proc:none','-encoding','UTF-8','-cp',classpath,str(WORK/'ExistingWeaponExtractor.java')],cwd=WORK,check=True)
subprocess.run(['java','-cp',classpath,'ExistingWeaponExtractor',str(PNG),str(WORK/'spear_in_hand.original.json'),str(WORK/'weapon_existing_generated.json')],cwd=WORK,check=True)
print('Now run prepare_existing_weapon.py to rebuild the native adapter input.')
