"""Canonical relic payouts and guaranteed per-player, per-boss ritual provisions."""
import json
from pathlib import Path
import sys
from rpg_catalogue import catalogue, resolve, give, max_stack
from make_boxes import parse_give
from extract_items import node_to_py, flatten
from rpg_ui_style import comp, row, HOLY, HOLY_LIGHT, HOLY_DARK, CYAN, GRAY

ROOT=Path(__file__).resolve().parent.parent
DP=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'rpg').resolve()
F=DP/'data/rpg/function'
CFG=json.loads((ROOT/'_endless_supplies.json').read_text(encoding='utf-8'))
ENDLESS=json.loads((ROOT/'_endless_exorcism_config.json').read_text(encoding='utf-8'))
RADIUS=ENDLESS['active_radius']


def write(rel,lines):
    p=F/rel;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(('\n'.join(lines) if isinstance(lines,list) else lines).rstrip()+'\n',encoding='utf-8')


def tell(*parts):return 'tellraw @s '+row(*parts)


def predicate(record):
    tag=next(v.dump() for k,v,neg,_ in record['block'].entries if k.split(':')[-1]=='custom_data' and not neg)
    return record['id']+'[minecraft:custom_data~'+tag+']'


def main():
    items=catalogue(DP)
    dispatch=[]
    for i,tier in enumerate(CFG['relic_tiers'],1):
        lo,hi=tier['tier']
        dispatch.append(f'execute if score #tier rpg_end_tmp matches {lo}..{hi} run function rpg:endless/reward/loot/{i}')
        write(f'endless/reward/loot/{i}.mcfunction',[give(items,n,c) for n,c in tier['items']]+[tell(comp('[遗珍] ',HOLY,True),comp('已收取数据包定制物资。',GRAY))])
    write('endless/reward/loot_dispatch.mcfunction',dispatch)
    bonus=['scoreboard players add @s rpg_ex_xp 12']
    for tier in CFG['boss_bonus']:
        lo,hi=tier['floor']
        for n,c in tier['items']:bonus.append(f'execute if score #floor rpg_end_tmp matches {lo}..{hi} run '+give(items,n,c))
    bonus.append(tell(comp('[领主宝库] ',HOLY_DARK,True),comp('已收取定制圣物与 12 点驱魔阅历。',HOLY_LIGHT)))
    write('endless/reward/boss_bonus.mcfunction',bonus)
    score=(F/'command/soreboard.mcfunction').read_text(encoding='utf-8').rstrip()
    for obj in ('rpg_end_supply','rpg_end_kit_id','rpg_end_kit_floor','rpg_end_kit_lord','rpg_end_need','rpg_end_free','rpg_end_have'):
        line=f'scoreboard objectives add {obj} '+('trigger' if obj=='rpg_end_supply' else 'dummy')
        if line not in score:score+='\n'+line
    write('command/soreboard.mcfunction',score)
    # Persist the selected lord on the controller; late joiners use the same kit.
    boss=(F/'endless/boss/dispatch.mcfunction').read_text(encoding='utf-8').splitlines()
    if not any('function rpg:endless/supply/request' in l for l in boss):
        idx=next(i for i,l in enumerate(boss) if l.startswith('execute if score #lord'))
        boss[idx:idx]=['scoreboard players operation @s rpg_end_kit_lord = #lord rpg_end_tmp',
                      f'execute as @a[tag=rpg.end.member.current,distance=..{RADIUS},gamemode=!spectator] at @s run function rpg:endless/supply/request']
    boss=[l.replace('distance=..96',f'distance=..{RADIUS}') if 'rpg:endless/supply/request' in l else l for l in boss]
    write('endless/boss/dispatch.mcfunction',boss)
    tick=(F/'endless/tick.mcfunction').read_text(encoding='utf-8').splitlines()
    if not any('rpg_end_supply' in l for l in tick):
        tick+=['scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_supply',
               'execute as @a[tag=rpg.end.member.current,scores={rpg_end_supply=1..}] at @s run function rpg:endless/supply/request',
               'scoreboard players set @a[tag=rpg.end.member.current,scores={rpg_end_supply=1..}] rpg_end_supply 0']
    write('endless/tick.mcfunction',tick)
    join=(F/'endless/join.mcfunction').read_text(encoding='utf-8').rstrip()
    if 'function rpg:endless/supply/request' not in join:join+='\nfunction rpg:endless/supply/request'
    write('endless/join.mcfunction',join)
    menu=(F/'panel/endless.mcfunction').read_text(encoding='utf-8').splitlines()
    if not any('rpg_end_supply' in l for l in menu):menu.append(tell(comp('[领主层补给]',HOLY,True,click_event={'action':'run_command','command':'/trigger rpg_end_supply set 1'}),comp('  每人每个领主层一次；背包满时可稍后领取。',GRAY)))
    write('panel/endless.mcfunction',menu)
    ctrl='@e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1]'
    request=[
        'execute unless entity @s[type=minecraft:player,tag=rpg.end.member.current,gamemode=!spectator] run return 0',
        'execute if entity @s[nbt={Health:0.0f}] run return 0',
        f'execute unless entity {ctrl} run return 0',
        f'execute unless score @s rpg_end_id = {ctrl} rpg_end_id run return 0',
        f'execute unless entity @e[type=minecraft:marker,tag=rpg.end.controller.current,distance=..{RADIUS}] run return 0',
        f'execute unless score {ctrl} rpg_end_state matches 1 run return 0',
        f'scoreboard players operation #supply_mod rpg_end_tmp = {ctrl} rpg_end_floor',
        'scoreboard players set #five rpg_end_tmp 5','scoreboard players operation #supply_mod rpg_end_tmp %= #five rpg_end_tmp',
        'execute unless score #supply_mod rpg_end_tmp matches 0 run return 0',
        # Existing sessions created before this update have no kit-lord score.
        # Recover it from the existing floor without restarting the encounter.
        f'scoreboard players operation #supply_lord rpg_end_tmp = {ctrl} rpg_end_floor',
        'scoreboard players operation #supply_lord rpg_end_tmp /= #five rpg_end_tmp',
        'scoreboard players remove #supply_lord rpg_end_tmp 1',
        'scoreboard players set #supply_seven rpg_end_tmp 7',
        'scoreboard players operation #supply_lord rpg_end_tmp %= #supply_seven rpg_end_tmp',
        'scoreboard players add #supply_lord rpg_end_tmp 1',
        f'scoreboard players operation {ctrl} rpg_end_kit_lord = #supply_lord rpg_end_tmp',
        f'execute if score @s rpg_end_kit_id = {ctrl} rpg_end_id if score @s rpg_end_kit_floor = {ctrl} rpg_end_floor run return 0']
    for lord in range(1,8):request.append(f'execute if score {ctrl} rpg_end_kit_lord matches {lord} run return run function rpg:endless/supply/kit{lord}')
    write('endless/supply/request.mcfunction',request)
    for lord in range(1,8):
        source=(F/f'inquest/give/medium{lord}.mcfunction').read_text(encoding='utf-8')
        parsed=next(parse_give(l) for l in source.splitlines() if parse_give(l))
        name=flatten(next(node_to_py(v) for k,v,neg,_ in parsed[1].entries if k.split(':')[-1]=='custom_name' and not neg))[0].split(']',1)[-1]
        kit=CFG['boss_kit']+[[name,CFG['medium_count']]]
        lines=['scoreboard players set @s rpg_end_need 0','scoreboard players set @s rpg_end_free 0']
        for slot in range(36):lines.append(f'execute unless entity @s[nbt={{Inventory:[{{Slot:{slot}b}}]}}] run scoreboard players add @s rpg_end_free 1')
        for n,count in kit:
            record=resolve(items,n);pred=predicate(record);stack=max_stack(record['id'],record['block'])
            lines.append(f'execute store result score @s rpg_end_have run clear @s {pred} 0')
            for have in range(count):
                needed=(count-have+stack-1)//stack
                lines.append(f'execute if score @s rpg_end_have matches {have} run scoreboard players add @s rpg_end_need {needed}')
        lines.append('execute if score @s rpg_end_free < @s rpg_end_need run return run '+tell(comp('[驱魔补给] ',HOLY,True),comp('请空出背包后领取；本层配额仍保留。',GRAY),comp('[领取]',CYAN,True,click_event={'action':'run_command','command':'/trigger rpg_end_supply set 1'})))
        for n,count in kit:
            pred=predicate(resolve(items,n))
            lines.append(f'execute store result score @s rpg_end_have run clear @s {pred} 0')
            for have in range(count):lines.append(f'execute if score @s rpg_end_have matches {have} run '+give(items,n,count-have))
        lines.extend([f'scoreboard players operation @s rpg_end_kit_id = {ctrl} rpg_end_id',
                      f'scoreboard players operation @s rpg_end_kit_floor = {ctrl} rpg_end_floor',
                      tell(comp('[驱魔补给] ',HOLY,True),comp('图腾、圣水、圣器、对应媒介与仪式工具已备齐。',HOLY_LIGHT)),
                      tell(comp('长按右键立起图腾，再以驱魔圣水点燃；调查真名后进入四阶段仪式。',GRAY))])
        write(f'endless/supply/kit{lord}.mcfunction',lines)
    print('endless supplies: 7 canonical relic tiers / canonical boss rewards / 7 guarded minimum ritual kits')


if __name__=='__main__':main()
