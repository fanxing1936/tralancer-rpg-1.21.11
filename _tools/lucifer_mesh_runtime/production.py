from pathlib import Path
import json,re,shutil

def dependencies(m,rp):
    src=rp; done={}
    def cp(rel):
        p=(rp/rel) if (rp/rel).exists() else src/rel
        if not p.exists():
            if Path(rel).parts[:2]==('assets','minecraft'):return
            raise FileNotFoundError(p)
        if str(rel) in done:return
        out=rp/rel;out.parent.mkdir(parents=True,exist_ok=True);
        if p.resolve()!=out.resolve():shutil.copyfile(p,out)
        done[str(rel)]=m.sha(p)
        if p.suffix=='.json':
            d=json.loads(p.read_text(encoding='utf-8'))
            def walk(x,key=''):
                if isinstance(x,dict):
                    for k,v in x.items():walk(v,k)
                elif isinstance(x,list):
                    for v in x:walk(v,key)
                elif isinstance(x,str) and ':' in x and not x.startswith('#'):
                    ns,name=x.split(':',1)
                    if key in ('parent','model') and not name.startswith(('model','range_dispatch','select')):cp(Path('assets')/ns/'models'/(name+'.json'))
            walk(d)
            for t in d.get('textures',{}).values():
                if ':' in t and not t.startswith('#'):
                    ns,name=t.split(':',1);cp(Path('assets')/ns/'textures'/(name+'.png'))
    cp(Path('assets/minecraft/items/netherite_spear.json'));cp(Path('assets/rpg/items/empty.json'))
    return done

def runtime(m,rig,rp,dp,baked,parts):
    K=m.KEY;T=m.TAG;S=m.SCORE;base=dp/f'data/rpg/function/{K}'
    def w(path,lines):m.write(base/(path+'.mcfunction'),'\n'.join(lines)+'\n')
    def f(path):return f'rpg:{K}/{path}'
    names=[p['name']for p in parts]+['weapon'];first=baked['rise']['frames'][0][1]
    w('load',[f'scoreboard objectives add {S}_{o} dummy' for o in ['anim','t','x','z','dx','dz','move','clock','hurt']])
    summon=[]
    for name in names:
        item='{id:"minecraft:netherite_spear",count:1,components:{"minecraft:custom_model_data":{floats:[1110014.0f]}}}' if name=='weapon' else '{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:'+K+'/'+name+'"}}'
        summon.append('summon minecraft:item_display ~ ~ ~ {Tags:["'+T+'.part","'+T+'.new","'+T+'.p.'+name+'"],item:'+item+',item_display:"'+('thirdperson_righthand' if name=='weapon' else 'none')+'",teleport_duration:2,interpolation_duration:1,view_range:1.5f,transformation:'+m.snbt(first[name])+'}')
    w('dress',['execute if entity @s[tag=rpg.lu.phase2] run return 0',f'execute if entity @s[tag={T}] run return 0',f'tag @s add {T}',f'tag @s add {T}.dressing']+summon+[
        f'execute as @e[type=minecraft:item_display,tag={T}.new,distance=..0.1] run ride @s mount @e[type=minecraft:vindicator,tag={T}.dressing,distance=..0.1,limit=1,sort=nearest]',
        f'tag @e[tag={T}.new,distance=..0.1] remove {T}.new',f'tag @s remove {T}.dressing',
        # Empty-handed carriers keep their original combat equipment/attributes.
        # The independent held display already contains the cosmetic spear.
        f'tag @s remove {T}.original_hand',
        f'execute if data entity @s equipment.mainhand.id run tag @s add {T}.original_hand',
        f'execute if entity @s[tag={T}.original_hand] run data modify storage rpg:{K} held set from entity @s equipment.mainhand',
        f'execute if entity @s[tag={T}.original_hand] on passengers if entity @s[tag={T}.p.weapon] run data modify entity @s item set from storage rpg:{K} held',
        f'execute if entity @s[tag={T}.original_hand] run data modify entity @s equipment.mainhand.components."minecraft:item_model" set value "rpg:empty"',
        f'scoreboard players set @s {S}_clock 0',f'function {f("movement/store")}',f'function {f("anim/enter/rise")}','effect give @s minecraft:invisibility infinite 0 true'])
    w('undress',[f'data modify storage rpg:{K} held set value {{}}',f'execute if entity @s[tag={T}.original_hand] on passengers if entity @s[tag={T}.p.weapon] run data modify storage rpg:{K} held set from entity @s item',f'execute if entity @s[tag={T}.original_hand] run data modify entity @s equipment.mainhand set from storage rpg:{K} held',f'execute on passengers if entity @s[tag={T}.part] run kill @s']+[f'tag @s remove {T}{suffix}' for suffix in ['', '.bound','.glow','.original_hand']])
    lord='type=minecraft:vindicator,tag=rpg.advent,tag=!rpg.lu,tag=!rpg.lu.phase2,scores={rpg_dm_lord=1}'
    w('tick',[f'execute as @e[tag={T},tag=rpg.lu.phase2] at @s run function {f("undress")}',f'execute as @e[{lord}] at @s run function {f("dress")}',f'execute as @e[type=minecraft:vindicator,tag={T},tag=!rpg.lu.phase2] at @s run function {f("follow")}',f'execute as @e[type=minecraft:item_display,tag={T}.part] unless predicate rpg:{K}/riding run kill @s'])
    w('tick_late',[f'execute as @e[type=minecraft:vindicator,tag={T},tag=!rpg.lu.phase2] run effect give @s minecraft:invisibility infinite 0 true'])
    w('movement/store',[f'execute store result score @s {S}_{axis} run data get entity @s Pos[{i}] 1000'for axis,i in [('x',0),('z',2)]])
    w('movement/check',[f'scoreboard players operation @s {S}_d{a} = @s {S}_{a}'for a in ['x','z']]+[f'function {f("movement/store")}']+[f'scoreboard players operation @s {S}_d{a} -= @s {S}_{a}'for a in ['x','z']]+[f'scoreboard players set @s {S}_move 0']+[f'execute unless score @s {S}_d{a} matches -3..3 run scoreboard players set @s {S}_move 1'for a in ['x','z']]+[f'execute if score @s {S}_anim matches 0 if score @s {S}_move matches 1 run function {f("anim/enter/walk")}',f'execute if score @s {S}_anim matches 1 if score @s {S}_move matches 0 run function {f("anim/enter/idle")}'])
    w('follow',[f'execute on passengers if entity @s[tag={T}.part] run rotate @s ~ 0',f'execute if entity @s[tag=rpg.exorcism.bound,tag=!{T}.bound] run function {f("bound/start")}',f'execute unless entity @s[tag=rpg.exorcism.bound] if entity @s[tag={T}.bound] run function {f("bound/end")}',f'scoreboard players add @s {S}_clock 1',f'execute if score @s {S}_clock matches 4.. run function {f("movement/check")}',f'execute if score @s {S}_clock matches 4.. run scoreboard players set @s {S}_clock 0',f'function {f("anim/tick")}'])
    for name,on in [('start',1),('end',0)]:w('bound/'+name,[f'tag @s {"add" if on else "remove"} {T}.bound',f'execute on passengers if entity @s[tag={T}.part] run data merge entity @s {{Glowing:{on}b}}',f'function {f("anim/enter/"+("stun" if on else "idle"))}'])
    # Terminal stun frame remains fixed until the bound tag clears.
    p=base/'anim/stun/tick.mcfunction';txt=p.read_text(encoding="utf-8");txt=txt.split('\n',1)[1];w('anim/stun/tick',[f'execute if score @s {S}_t matches {baked["stun"]["ticks"]+1}.. run return 0',txt.rstrip()])
    for clip in m.ORDER:
        w('play/'+clip,['execute if entity @s[tag=rpg.lu.phase2] run return 0',f'execute if entity @s[tag={T}.bound] run return 0',f'function {f("anim/enter/"+clip)}'])
    for hook,clip in m.SKILLS.items():w('skill/'+hook,[f'function {f("play/"+clip)}'])
    # Isolated pack hook order; production owner must append tick_late after command/tick_end.
    m.merge_tag(dp,'tick',f('tick'))
    # Move late hide to the end of the existing tick list, after command/tick_end.
    tagpath=dp/'data/minecraft/tags/function/tick.json';tagdoc=json.loads(tagpath.read_text(encoding='utf-8'));tagdoc['values']=[v for v in tagdoc['values'] if v!=f('tick_late')]+[f('tick_late')];m.js(tagpath,tagdoc)
    sounds={};source=m.REPO/'_tools/lucifer_ref/sounds'
    for group in ['attack','death','hurt','idle','step','arrowwhoosh']:
        files=sorted(p for p in source.glob('*.ogg') if re.search(group,p.stem,re.I));entries=[]
        for p in files:
            rel=f'{K}/{p.stem.lower()}';out=rp/f'assets/rpg/sounds/{rel}.ogg';out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out);entries.append({'name':'rpg:'+rel,'stream':False})
        if files:sounds[f'{K}.{group}']={'sounds':entries};w('sound/'+group,[f'playsound rpg:{K}.{group} hostile @a[distance=..48] ~ ~ ~ 1 1'])
    soundpath=rp/'assets/rpg/sounds.json';all_sounds=json.loads(soundpath.read_text(encoding='utf-8')) if soundpath.exists() else {};all_sounds.update(sounds);m.js(soundpath,all_sounds)
    # Animation cues do not alter combat timing or damage.
    cue_map={'attack':[(0,'attack')],'strong':[(0,'attack'),(8,'arrowwhoosh')],'cast':[(0,'arrowwhoosh')],'slash':[(0,'attack'),(3,'arrowwhoosh')],'walk':[(0,'step'),(8,'step')],'laugh':[(0,'idle')],'rise':[(0,'idle')]}
    for clip,cues in cue_map.items():
        if clip not in baked:continue
        for tick,sound in cues:
            path=base/f'anim/{clip}/f{tick}.mcfunction'
            if path.exists():m.write(path,path.read_text(encoding='utf-8')+f'function {f("sound/"+sound)}\n')
    follow=base/'follow.mcfunction';m.write(follow,follow.read_text(encoding='utf-8')+f'execute store result score @s {S}_hurt run data get entity @s HurtTime\nexecute if score @s {S}_hurt matches 10 run function {f("sound/hurt")}\nexecute if predicate rpg:{K}/ambient run function {f("sound/idle")}\n')
    m.js(dp/f'data/rpg/predicate/{K}/ambient.json',{'condition':'minecraft:random_chance','chance':0.006})
    w('orphan',[f'execute if entity @s[tag={T}.p.weapon] run function {f("sound/death")}','kill @s'])
    tick=base/'tick.mcfunction';m.write(tick,tick.read_text(encoding='utf-8').replace('unless predicate rpg:'+K+'/riding run kill @s','unless predicate rpg:'+K+'/riding at @s run function '+f('orphan')))

    return {'sound_files':sum(len(x['sounds']) for x in sounds.values()),'tick_late_order':'root must append after rpg:command/tick_end','phase_guard':'rpg.lu.phase2'}
