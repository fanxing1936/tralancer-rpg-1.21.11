"""Strict coexistence contract for P1/P2/vanilla 1.21.11 core shaders."""
from pathlib import Path
import re,hashlib

class VanillaArchive:
    def __init__(self,root):self.root=Path(root)
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,name):
        if not name.startswith('assets/minecraft/shaders/core/'):raise ValueError('No unverified bundled include: '+name)
        return (self.root/Path(name).name).read_bytes()

def phase2_sources(repo,owner,archive):
    out={}
    for ext in ['vsh','fsh']:
        vanilla=archive.read('assets/minecraft/shaders/core/'+owner.SHADER_NAME+'.'+ext).decode()
        if hashlib.sha256(vanilla.encode()).hexdigest()!=owner.VANILLA_SHADER_SHA256[ext]:raise ValueError('Bundled vanilla shader checksum mismatch')
        if ext=='vsh':
            current=vanilla.replace('void main() {',owner.VERTEX_DECL+'\nvoid main() {',1);close=current.rfind('}');current=current[:close]+owner.VERTEX_MAIN+current[close:]
            assert current.replace(owner.VERTEX_DECL+'\n','',1).replace(owner.VERTEX_MAIN,'',1)==vanilla
        else:
            current=vanilla.replace('void main() {',owner.FRAGMENT_DECL+'\nvoid main() {\n'+owner.FRAGMENT_MAIN,1)
            assert current.replace(owner.FRAGMENT_DECL+'\n','',1).replace('\n'+owner.FRAGMENT_MAIN,'',1)==vanilla
        reference=Path(repo)/'_tools/lucifer_p2_ref/material/rp/assets/minecraft/shaders/core'/(owner.SHADER_NAME+'.'+ext)
        if not reference.exists() or reference.read_bytes()!=current.encode():raise ValueError('Phase2 generated shader differs from its owning source; regenerate/review phase2 material before combining: '+str(reference))
        out[ext]=current
    return out

def mark_block(kind,text):return '// BEGIN LUCIFER_P1_MESH '+kind+'\n'+text.rstrip('\n')+'\n// END LUCIFER_P1_MESH '+kind+'\n'

def strip_p1(text):
    pattern=r'// BEGIN LUCIFER_P1_MESH DECL\n.*?// END LUCIFER_P1_MESH DECL\n\nvoid main\(\) \{\n// BEGIN LUCIFER_P1_MESH MAIN\n.*?// END LUCIFER_P1_MESH MAIN\n'
    stripped,n=re.subn(pattern,'void main() {',text,flags=re.S)
    if n>1:raise ValueError('Multiple P1 shader insertion blocks')
    return stripped

def guarded_write_shader(path,text,vanilla,phase2):
    path=Path(path)
    if path.exists():
        current=path.read_bytes().decode('utf-8')
        if current!=text and strip_p1(current) not in [vanilla,phase2]:raise ValueError('Unknown core shader override; explicit review required: '+str(path))
    if strip_p1(text)!=phase2:raise ValueError('P1 removal does not restore verified predecessor')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(text.encode())

def prepare_deferred_shaders(rp,repo,vanilla_root):
    from dungeons_conversion import materials
    with VanillaArchive(vanilla_root) as archive:
        p2=phase2_sources(repo,materials,archive)
        for kind in [materials.SHADER_NAME,'rendertype_outline']:
            for ext in ['vsh','fsh']:
                target=Path(rp)/'assets/minecraft/shaders/core'/(kind+'.'+ext)
                if not target.exists():continue
                vanilla=archive.read('assets/minecraft/shaders/core/'+target.name).decode();prior=p2[ext] if kind==materials.SHADER_NAME else vanilla
                stripped=strip_p1(target.read_bytes().decode())
                if stripped not in [vanilla,prior]:raise ValueError('Cannot defer unknown shader: '+str(target))
                target.write_bytes(stripped.encode())
