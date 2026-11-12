"""Phase-two appearance controller. Phase signals remain externally owned."""
from pathlib import Path
import json,re
from display_mob import NS,wf,wj,hook_tag,write_rig_runtime,snbt_components,playsound
from . import materials,sounds

def write(mob,baked,first,ref):
    folder=Path(mob.func);dp=Path(mob.dp)
    def fn(name,lines):wf(str(folder/(name+'.mcfunction')),lines)
    base='type=minecraft:vindicator,scores={rpg_dm_lord=1}'
    pulse={p['name'] for p in json.loads((Path(ref)/'parts.json').read_text(encoding='utf-8')) if p.get('glow_bones')}
    dress=['# 二阶段外观；外部 rpg.lu.phase2 只读。',
           'execute unless entity @s[%s,tag=rpg.lu.phase2] run return 0'%base,
           'execute if entity @s[tag=rpg.lu2] run return 0',
           # Phase one owns its held-item backup. Let it restore that state
           # before fallback cleanup, including direct calls before P1's tick.
           'execute if entity @s[tag=rpg.lu] run function #rpg:lucifer_p2/phase1_leave',
           'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu.part] run kill @s',
           'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run kill @s',
           'tag @s remove rpg.lu','tag @s remove rpg.lu.dressing','tag @s remove rpg.lu.glow',
           'tag @s remove rpg.lu.bound','tag @s remove rpg.lu.original_hand',
           'tag @s add rpg.lu2','tag @s remove rpg.lu2.death_played',
           'data modify storage rpg:lucifer_p2 mount.uuid set from entity @s UUID']
    for part,comp in first:
        tags=['rpg.lu2.part','rpg.lu2.p.'+part,'rpg.lu2.new']+(['rpg.lu2.pulse'] if part in pulse else [])
        dress.append('summon minecraft:item_display ~ ~ ~ {Tags:%s,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_p2/%s","minecraft:custom_data":{part:"%s"},"minecraft:custom_model_data":{colors:%s}}},item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:3f,transformation:%s}' % (
            json.dumps(tags,separators=(',',':')),part,part,json.dumps(materials.INITIAL_COLORS,separators=(',',':')),snbt_components(mob,comp)))
    dress += ['execute as @e[type=minecraft:item_display,tag=rpg.lu2.new,distance=..1] run function rpg:lucifer_p2/mount with storage rpg:lucifer_p2 mount',
              'tag @e[type=minecraft:item_display,tag=rpg.lu2.new,distance=..1] remove rpg.lu2.new',
              'function rpg:lucifer_p2/anim/init',
              'function rpg:lucifer_p2/anim/enter/'+mob.idle_clip]
    fn('dress',dress)
    fn('mount',['# Exact owning carrier UUID; overlapping lords cannot steal parts.',
                '$ride @s mount @e[type=minecraft:vindicator,nbt={UUID:$(uuid)},limit=1]'])
    fn('undress',['# Only this carrier\'s phase-two displays; no death sound on switch.',
        'execute unless entity @s[tag=rpg.lu2] run return 0',
        'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run kill @s',
        'tag @s remove rpg.lu2','tag @s remove rpg.lu2.glow','tag @s remove rpg.lu2.death_played',
        'tag @s remove rpg.lu2.flower',
    ]+['scoreboard players reset @s '+s for s in (mob.clip_score,mob.t_score,mob.score+'_mv',mob.score+'_mc',mob.score+'_x',mob.score+'_z',mob.score+'_flower')]+[
        'execute if score @s rpg_dm_lord matches 1 unless entity @s[tag=rpg.lu] run function #rpg:lucifer_p2/phase1_return'])
    # Optional existing phase-one controller. Missing phase-one assets do not
    # invent a substitute model or create an unresolved function reference.
    wj(str(dp/'data/rpg/tags/function/lucifer_p2/phase1_return.json'),{
        'values':[{'id':'rpg:lucifer_lord/dress','required':False}]})
    wj(str(dp/'data/rpg/tags/function/lucifer_p2/phase1_leave.json'),{
        'values':[{'id':'rpg:lucifer_lord/undress','required':False}]})
    write_rig_runtime(mob,[
        '# Appearance only: no add/remove of the external phase signal.',
        'function rpg:lucifer_p2/material/tick',
        'execute as @e[type=minecraft:vindicator,tag=rpg.lu2,tag=!rpg.lu.phase2] at @s run function rpg:lucifer_p2/undress',
        'execute as @e[type=minecraft:vindicator,tag=rpg.lu2] at @s unless score @s rpg_dm_lord matches 1 run function rpg:lucifer_p2/undress',
        'execute as @e[%s,tag=rpg.lu.phase2,tag=!rpg.lu2] at @s run function rpg:lucifer_p2/dress'%base,
        'execute as @e[%s,tag=rpg.lu.phase2,tag=rpg.lu2] at @s run function rpg:lucifer_p2/follow'%base,
    ],follow_extra=[
        'execute if predicate rpg:lucifer_p2/glowing unless entity @s[tag=rpg.lu2.glow] run function rpg:lucifer_p2/glow_on',
        'execute unless predicate rpg:lucifer_p2/glowing if entity @s[tag=rpg.lu2.glow] run function rpg:lucifer_p2/glow_off',
        'execute if entity @s[tag=rpg.lu2.flower] run function rpg:lucifer_p2/flower/tick',
    ])
    # Scope the template's rotation to our own displays, preserving soul markers.
    path=folder/'follow.mcfunction';text=path.read_text(encoding='utf-8')
    text=text.replace('execute on passengers run rotate @s ~ 0',
                      'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run rotate @s ~ 0')
    path.write_text(text,encoding='utf-8',newline='\n')
    wj(str(dp/'data/rpg/predicate/lucifer_p2/riding.json'),{
        'condition':'minecraft:entity_properties','entity':'this',
        # A vehicle NBT predicate serializes the carrier AND all passengers for
        # every display in the orphan scan. Use the native type test; explicit
        # undress handles ownership/state changes without quadratic NBT work.
        'predicate':{'vehicle':{'type':'minecraft:vindicator'}}})
    for name,effect in [('glowing','minecraft:glowing'),('invisible','minecraft:invisibility')]:
        wj(str(dp/'data/rpg/predicate/lucifer_p2'/(name+'.json')),{
            'condition':'minecraft:entity_properties','entity':'this','predicate':{'effects':{effect:{}}}})
    for name,on in [('glow_on',1),('glow_off',0)]:
        fn(name,['tag @s %s rpg.lu2.glow'%('add' if on else 'remove'),
                 'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run data merge entity @s {Glowing:%db}'%on])
    fn('tick_late',['# After command/tick_end: the appearance carrier remains hidden.',
        'execute as @e[%s,tag=rpg.lu2,tag=rpg.lu.phase2] unless predicate rpg:lucifer_p2/invisible run effect give @s minecraft:invisibility infinite 0 true'%base])
    hook_tag(mob.dp,'tick','rpg:lucifer_p2/tick_late',False)
    # All entity paths own their sound state. A phase switch never triggers death.
    fn('death',['# Orphan-anchor fallback; explicit death clip has already voiced it.',
        'execute unless entity @s[tag=rpg.lu2.death_played] run '+playsound(mob,sounds.DEATH,mob.death_volume,radius=48),
        'execute unless entity @s[tag=rpg.lu2.death_played] run '+playsound(mob,sounds.DEATH_FOLEY,1.,radius=48)])
    ids={name:i for i,(name,_,_) in enumerate(mob.clips)}
    fn('flower/tick',[
        'execute unless score @s rpg_lu2_anim matches %d unless score @s rpg_lu2_anim matches %d run return run function rpg:lucifer_p2/flower/stop'%(
            ids['jungleabomination_vulnerablefall'],ids['jungleabomination_vulnerablestuncycle']),
        'scoreboard players remove @s rpg_lu2_flower 1',
        'execute if score @s rpg_lu2_flower matches ..0 run function rpg:lucifer_p2/flower/repeat'])
    fn('flower/repeat',[playsound(mob,'flower_loop',1.),'scoreboard players set @s rpg_lu2_flower 87'])
    fn('flower/start',['tag @s add rpg.lu2.flower','scoreboard players set @s rpg_lu2_flower 88'])
    fn('flower/stop',['tag @s remove rpg.lu2.flower','scoreboard players reset @s rpg_lu2_flower'])
    for name,_,_ in mob.clips:
        lines=['# Public single-carrier entry; no combat/phase-condition changes.',
               'execute unless entity @s[%s,tag=rpg.lu.phase2,tag=rpg.lu2] run return 0'%base]
        if name.endswith('_death'):
            lines+=['tag @s add rpg.lu2.death_played',
                    'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run tag @s add rpg.lu2.death_played',
                    'function rpg:lucifer_p2/flower/stop']
        else:
            lines+=['tag @s remove rpg.lu2.death_played',
                    'execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run tag @s remove rpg.lu2.death_played']
        if name.endswith('_vulnerablegetup'):
            lines+=['function rpg:lucifer_p2/flower/stop']
        lines+=['return run function rpg:lucifer_p2/anim/enter/'+name]
        fn('play/'+name,lines)
    # The raw notify retains its exact tick; the target repeat timer starts there.
    for file in (folder/'anim').rglob('f*.mcfunction'):
        text=file.read_text(encoding='utf-8')
        if 'playsound rpg:lucifer_p2.flower_loop ' in text:
            text+='function rpg:lucifer_p2/flower/start\n'
            file.write_text(text,encoding='utf-8',newline='\n')
    load=folder/'load.mcfunction'
    with load.open('a',encoding='utf-8',newline='\n') as stream:
        stream.write('scoreboard objectives add rpg_lu2_mat dummy\nscoreboard objectives add rpg_lu2_flower dummy\n')
        stream.write('execute unless score #phase rpg_lu2_mat matches 0..199 run scoreboard players set #phase rpg_lu2_mat 0\n')
    fn('material/tick',['# Shared 200-tick source pulse; only eight emissive parts write tint.',
        'scoreboard players add #phase rpg_lu2_mat 1',
        'execute if score #phase rpg_lu2_mat matches 200.. run scoreboard players set #phase rpg_lu2_mat 0',
        'scoreboard players set #color rpg_lu2_mat %d'%materials.GLOW_MARKER,
        'scoreboard players operation #color rpg_lu2_mat += #phase rpg_lu2_mat',
        'execute store result storage rpg:lucifer_p2 material.glow_color int 1 run scoreboard players get #color rpg_lu2_mat',
        'execute as @e[type=minecraft:item_display,tag=rpg.lu2.pulse] run data modify entity @s item.components."minecraft:custom_model_data".colors[2] set from storage rpg:lucifer_p2 material.glow_color'])
    fn('debug/summon',['# Summon the existing lord. Add the external phase tag manually to enter phase two.',
        'function rpg:taint/lord1'])
    # One public caller debug command for each clip, operating on nearby carriers.
    for name,_,_ in mob.clips:
        fn('debug/play/'+name,['execute as @e[%s,tag=rpg.lu2,sort=nearest,limit=1,distance=..32] at @s run function rpg:lucifer_p2/play/%s'%(base,name)])
    return {'parts':len(mob.parts),'pulse_parts':len(pulse),'bulk_pose':mob.bulk_pose,
            'optional_phase1_dress_present':(dp/'data/rpg/function/lucifer_lord/dress.mcfunction').exists(),
            'phase_signal_written_by_controller':False,
            'debug_signal_command':'None: user/test harness/future combat owns all phase-signal writes.',
            'flower_loop_policy':'Per-carrier 87-tick replay; stop cancels future repeats. Existing Ogg can ring out for <=4.326s; no global stopsound that would mute another carrier.',
            'phase1_leave':'Optional undress callback before cleanup restores phase-one-owned held-item state, independent of tick order.',
            'phase1_return':'Optional function tag; final stage-one Java renderer is owned by its separate task.'}

def guard_phase1_entry(datapack):
    """Add the phase exclusion to generated phase-one dressing selectors only."""
    path=Path(datapack)/'data/rpg/function/lucifer_lord/tick.mcfunction'
    if not path.exists():return {'phase1_entry_present':False,'guards_added':0}
    text=path.read_text(encoding='utf-8');count=0
    def replace(match):
        nonlocal count
        selector=match.group(0)
        if 'rpg_dm_lord=1' in selector and re.search(r'(?:\[|,)tag=!rpg\.lu(?:,|\])',selector) and 'rpg.lu.phase2' not in selector:
            count+=1;return selector[:-1]+',tag=!rpg.lu.phase2]'
        return selector
    updated=re.sub(r'@e\[[^\]]+\]',replace,text)
    if updated!=text:path.write_text(updated,encoding='utf-8',newline='\n')
    return {'phase1_entry_present':True,'guards_added':count,'scope':'Generated dressing selectors only; phase-one source/model untouched.'}
