"""Copy the stopped private test world and enable its local test commands."""
from pathlib import Path
import gzip, io, json, shutil, struct

ROOT=Path(__file__).resolve().parent
FORMATS={1:'b',2:'h',3:'i',4:'q',5:'f',6:'d'}

def num(f,fmt):return struct.unpack('>'+fmt,f.read(struct.calcsize(fmt)))[0]
def string(f):return f.read(num(f,'H')).decode('utf-8')
def read_value(f,t):
    if t in FORMATS:return num(f,FORMATS[t])
    if t==7:return f.read(num(f,'i'))
    if t==8:return string(f)
    if t==9:
        child=num(f,'B');return (child,[read_value(f,child) for _ in range(num(f,'i'))])
    if t==10:
        d={}
        while (child:=num(f,'B')):
            name=string(f);d[name]=(child,read_value(f,child))
        return d
    if t in (11,12):return [num(f,'i' if t==11 else 'q') for _ in range(num(f,'i'))]
    raise ValueError(t)
def pack(fmt,v):return struct.pack('>'+fmt,v)
def put_string(v):
    b=v.encode('utf-8');return pack('H',len(b))+b
def write_value(t,v):
    if t in FORMATS:return pack(FORMATS[t],v)
    if t==7:return pack('i',len(v))+v
    if t==8:return put_string(v)
    if t==9:return pack('B',v[0])+pack('i',len(v[1]))+b''.join(write_value(v[0],x) for x in v[1])
    if t==10:return b''.join(pack('B',ct)+put_string(k)+write_value(ct,cv) for k,(ct,cv) in v.items())+b'\0'
    if t in (11,12):return pack('i',len(v))+b''.join(pack('i' if t==11 else 'q',x) for x in v)
    raise ValueError(t)

status=json.loads((ROOT/'server/status.json').read_text())
assert status.get('exit_code')==0,status
source=ROOT/'server/packtest'
dest=ROOT/'game/saves/LuciferP2-Isolated'
assert not dest.exists(),'Do not overwrite an existing test save'
shutil.copytree(source,dest)
p=dest/'level.dat'
original=gzip.decompress(p.read_bytes())
f=io.BytesIO(original);t=num(f,'B');name=string(f);root=read_value(f,t)
assert f.tell()==len(original)
assert pack('B',t)+put_string(name)+write_value(t,root)==original,'NBT codec must preserve unmodified bytes'
data=root['Data'][1]
data['allowCommands']=(1,1)
data['LevelName']=(8,'Lucifer Phase 2 - Isolated Validation')
data['GameType']=(3,3)
data['Difficulty']=(1,2)
p.write_bytes(gzip.compress(pack('B',t)+put_string(name)+write_value(t,root)))
testpack=dest/'datapacks/p2_visual_test'
fn=testpack/'data/p2_visual/function'
fn.mkdir(parents=True)
(testpack/'pack.mcmeta').write_text(json.dumps({'pack':{'min_format':[94,1],'max_format':[94,1],'description':'Local p2 visual test fixture'}}))
setup='''gamemode spectator @s
tp @s 0 70 28 180 4
execute as @e[tag=p2_client_npc,limit=1] at @s run function rpg:lucifer_p2/anim/jungleabomination_idle/f0
scoreboard players set @e[tag=p2_client_npc,limit=1] rpg_lu2_anim 99
execute as @e[type=minecraft:item_display,tag=rpg.lu2.pulse] run data modify entity @s item.components."minecraft:custom_model_data".colors[2] set value 2544434
'''
(fn/'setup.mcfunction').write_text(setup,encoding='utf-8')
for phase in (50,150):
    (fn/('phase'+str(phase)+'.mcfunction')).write_text('execute as @e[type=minecraft:item_display,tag=rpg.lu2.pulse] run data modify entity @s item.components."minecraft:custom_model_data".colors[2] set value '+str(2544384+phase)+'\n',encoding='utf-8')
print(dest)
