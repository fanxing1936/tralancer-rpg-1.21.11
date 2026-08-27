"""Generate paid prayer, durable pending rewards, animation and exact odds from one pool."""
import json
import math
from pathlib import Path
import sys
from rpg_catalogue import catalogue, resolve, give, max_stack
from extract_items import flatten

ROOT = Path(__file__).resolve().parent.parent
DP = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'rpg').resolve()
F = DP / 'data/rpg/function'
CFG = json.loads((ROOT / '_prayer_pool.json').read_text(encoding='utf-8'))
CURRENCY = 'minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}]'


def write(rel, lines):
    p = F / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(('\n'.join(lines) if isinstance(lines, list) else lines).rstrip() + '\n', encoding='utf-8')


def text(t, c='#AAB4C3', bold=False, command=None):
    out = {'text':t,'color':c,'bold':bold,'italic':False}
    if command:
        out['click_event']={'action':'run_command','command':command}
    return out


def msg(*parts):
    return 'tellraw @s ' + json.dumps(['', *[text(p) if isinstance(p,str) else p for p in parts]], ensure_ascii=False, separators=(',', ':'))


def percent(weight):
    return f'{weight * 100 / CFG["total_weight"]:.2f}%'


def build_currency(items):
    # Repair all authored currency drops, without accepting ordinary raw gold.
    legacy = []
    coin = resolve(items,'货币')['components']
    legacy.append((coin['custom_name'],coin['lore']))
    changed = 0
    for p in (DP / 'data').glob('*/loot_table/**/*.json'):
        doc = json.loads(p.read_text(encoding='utf-8'))
        dirty = False
        def visit(node):
            nonlocal dirty
            if isinstance(node,list):
                for v in node: visit(v)
            elif isinstance(node,dict):
                if isinstance(node.get('name'),str) and node['name'].split(':')[-1] == 'raw_gold':
                    funcs = node.get('functions',[])
                    names = [f.get('name') for f in funcs if f.get('function','').split(':')[-1]=='set_name']
                    lores = [f.get('lore') for f in funcs if f.get('function','').split(':')[-1]=='set_lore']
                    if any('[currency]' in flatten(n)[0] for n in names):
                        if names and lores: legacy.append((names[0],lores[0]))
                        marker={'function':'minecraft:set_custom_data','tag':'{currency_tag:1b}'}
                        if marker not in funcs:
                            node.setdefault('functions',[]).append(marker)
                            dirty=True
                for v in node.values(): visit(v)
        visit(doc)
        if dirty:
            p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            changed += 1
    modifier = DP / 'data/rpg/item_modifier/prayer/mark_currency.json'
    modifier.parent.mkdir(parents=True,exist_ok=True)
    modifier.write_text(json.dumps({'function':'minecraft:set_custom_data','tag':'{currency_tag:1b}'})+'\n',encoding='utf-8')
    lines=['# 仅兼容精确匹配既有货币名称与整段 lore、尚无 custom_data 的旧币。']
    seen=set()
    for name,lore in legacy:
        # sort_keys 不是洁癖：name/lore 是从既有 give 命令解析回来的字典，
        # 键序随解析来源浮动，于是同样的输入两次构建会写出不同的字节，
        # git status 永远是脏的、diff 也失去意义。JSON 对象本就无序，
        # 排一下键既不改变 Minecraft 的解析结果，又让构建可复现。
        signature=json.dumps([name,lore],ensure_ascii=False,separators=(',',':'),sort_keys=True)
        if signature in seen: continue
        seen.add(signature)
        predicate='minecraft:raw_gold[minecraft:custom_name='+json.dumps(name,ensure_ascii=False,separators=(',',':'),sort_keys=True)+',minecraft:lore='+json.dumps(lore,ensure_ascii=False,separators=(',',':'),sort_keys=True)+',!minecraft:custom_data]'
        for slot in [f'hotbar.{i}' for i in range(9)]+[f'inventory.{i}' for i in range(27)]+['weapon.offhand']:
            lines.append(f'execute if items entity @s {slot} {predicate} run item modify entity @s {slot} rpg:prayer/mark_currency')
    write('prayer/currency.mcfunction',lines)
    write('prayer/debug/coins.mcfunction',['execute unless entity @s[type=minecraft:player] run return 0',give(items,'货币',64)])
    return changed


def main():
    entries=CFG['entries']; groups={g['id']:g for g in CFG['groups']}; items=catalogue(DP)
    assert sum(e['weight'] for e in entries)==CFG['total_weight']==10000
    assert len({e['key'] for e in entries})==len(entries)
    for e in entries:
        item=resolve(items,e['name'])
        assert 0 < e['count'] <= max_stack(item['id'],item['block'])
        assert e['group'] in groups and e['weight'] > 0
    currency_changes=build_currency(items)
    cost=CFG['cost']; ticks=CFG['animation_ticks']
    objectives=['rpg_pray','rpg_pr_have','rpg_pr_space','rpg_pr_pending','rpg_pr_time','rpg_pr_roll','rpg_pr_paid','rpg_pr_total']
    score=(F/'command/soreboard.mcfunction').read_text(encoding='utf-8').rstrip()
    for obj in objectives:
        line=f'scoreboard objectives add {obj} '+('trigger' if obj=='rpg_pray' else 'dummy')
        if line not in score: score+='\n'+line
    write('command/soreboard.mcfunction',score)
    tick=(F/'command/tick.mcfunction').read_text(encoding='utf-8').rstrip()
    if 'function rpg:prayer/tick' not in tick: tick+='\nfunction rpg:prayer/tick'
    write('command/tick.mcfunction',tick)
    panel=(F/'panel/tick.mcfunction').read_text(encoding='utf-8')
    route='execute if score @s rpg_panel matches 18 run function rpg:prayer/menu'
    if route not in panel: panel=panel.replace('execute if score @s rpg_panel matches 1..',route+'\nexecute if score @s rpg_panel matches 1..')
    write('panel/tick.mcfunction',panel)
    panel=(F/'panel/open.mcfunction').read_text(encoding='utf-8').splitlines()
    panel=[l for l in panel if '/trigger rpg_panel set 18' not in l]
    panel.insert(-2,msg(text('[圣所祷告]','#FFD85A',True,'/trigger rpg_panel set 18'),f'  每次 {cost} 枚货币 · 查看奖池与概率'))
    write('panel/open.mcfunction',panel)
    write('prayer/tick.mcfunction',[
        'scoreboard players enable @a rpg_pray',
        'execute as @a[scores={rpg_pr_time=1..}] at @s run function rpg:prayer/animate',
        'execute as @a[scores={rpg_pray=1}] at @s run function rpg:prayer/menu',
        'execute as @a[scores={rpg_pray=2}] at @s run function rpg:prayer/start',
        'execute as @a[scores={rpg_pray=3}] at @s run function rpg:prayer/pool',
        'execute as @a[scores={rpg_pray=4}] at @s run function rpg:prayer/claim',
        'scoreboard players set @a[scores={rpg_pray=1..}] rpg_pray 0'])
    write('prayer/space.mcfunction',['scoreboard players set @s rpg_pr_space 0']+[
        f'execute unless entity @s[nbt={{Inventory:[{{Slot:{i}b}}]}}] run scoreboard players set @s rpg_pr_space 1' for i in range(36)])
    write('prayer/menu.mcfunction',[
        'execute unless entity @s[type=minecraft:player] run return 0',
        'function rpg:prayer/currency',f'execute store result score @s rpg_pr_have run clear @s {CURRENCY} 0',
        msg(text('+------ 圣所祷告 · 耶和华 ------+','#D4AF37',True)),
        msg('奉上货币，静候恩赐。'),
        msg('持有 ',{'score':{'name':'@s','objective':'rpg_pr_have'},'color':'#FFF2A8','bold':False,'italic':False},f' 枚  ·  一次祷告 {cost} 枚'),
        msg(text('[祷告一次]','#FFD85A',True,'/trigger rpg_pray set 2'),'  ',text('[奖池与概率]','#62D9E8',True,'/trigger rpg_pray set 3'),'  ',text('[返回面板]','#AAB4C3',True,'/trigger rpg_panel set 8')),
        'execute if score @s rpg_pr_pending matches 1.. run '+msg(text('[领取待领恩赐]','#FFF2A8',True,'/trigger rpg_pray set 4'),'  已扣费的奖品不再收费。'),
        msg('普通粗金不计入货币；固定概率，无保底，可重复获得。'),
        msg(text('+--------------------------+','#D4AF37',True))])
    for key,message in [('poor','货币不足；本次未扣费。'),('full','请在背包中空出一格；本次未扣费。'),('busy','祷告正在进行，请静候恩赐。'),('pending','恩赐已为你保留；空出背包后点击领取，不再扣费。')]:
        write(f'prayer/error/{key}.mcfunction',[msg(text('[祷告]','#D4AF37',True),text(message,'#FFF2A8' if key in ('busy','pending') else '#FF665E'))])
    write('prayer/start.mcfunction',[
        'execute unless entity @s[type=minecraft:player,gamemode=!spectator] run return 0',
        'execute if entity @s[nbt={Health:0.0f}] run return 0',
        'execute if score @s rpg_pr_time matches 1.. run return run function rpg:prayer/error/busy',
        'execute if score @s rpg_pr_pending matches 1.. run return run function rpg:prayer/claim',
        'function rpg:prayer/currency',f'execute store result score @s rpg_pr_have run clear @s {CURRENCY} 0',
        f'execute unless score @s rpg_pr_have matches {cost}.. run return run function rpg:prayer/error/poor',
        'function rpg:prayer/space',
        'execute unless score @s rpg_pr_space matches 1 run return run function rpg:prayer/error/full',
        f'execute store result score @s rpg_pr_paid run clear @s {CURRENCY} {cost}',
        f'execute unless score @s rpg_pr_paid matches {cost} run return 0',
        'execute store result score @s rpg_pr_roll run random value 1..10000 rpg:prayer',
        'function rpg:prayer/select',f'scoreboard players set @s rpg_pr_time {ticks}',
        'scoreboard players add @s rpg_pr_total 1',
        msg(text('[祷告]','#D4AF37',True),'光正在回应你的祈愿。'),
        'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.45 1.05'])
    bounds=[]; start=1; select=[]; dispatch=[]
    for index,e in enumerate(entries,1):
        end=start+e['weight']-1; bounds.append((e,start,end))
        select.append(f'execute if score @s rpg_pr_roll matches {start}..{end} run scoreboard players set @s rpg_pr_pending {index}')
        dispatch.append(f'execute if score @s rpg_pr_pending matches {index} run return run function rpg:prayer/reward/{e["key"]}')
        write(f'prayer/reward/{e["key"]}.mcfunction',[
            give(items,e['name'],e['count']),
            'scoreboard players set @s rpg_pr_pending 0',
            msg(text('[恩赐]','#D4AF37',True),'祷告已被垂听。获得：',text(e['name'],groups[e['group']]['color']),f' ×{e["count"]}'),
            'particle minecraft:end_rod ~ ~1 ~ 0.35 0.55 0.35 0.02 8 normal @s',
            'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.5 1.5'])
        start=end+1
    write('prayer/select.mcfunction',select)
    write('prayer/claim.mcfunction',[
        'execute unless entity @s[type=minecraft:player,gamemode=!spectator] run return 0',
        'execute if entity @s[nbt={Health:0.0f}] run return 0',
        'execute if score @s rpg_pr_time matches 1.. run return run function rpg:prayer/error/busy',
        'execute unless score @s rpg_pr_pending matches 1.. run return 0',
        'function rpg:prayer/space',
        'execute unless score @s rpg_pr_space matches 1 run return run function rpg:prayer/error/pending',*dispatch])
    animate=['execute if entity @s[nbt={Health:0.0f}] run return 0','execute if entity @s[gamemode=spectator] run return 0',
             'scoreboard players remove @s rpg_pr_time 1']
    for moment in (35,25,15,5):
        rel=f'prayer/fx/{moment}'; lines=[]
        for point in range(8):
            angle=point*math.pi/4+(35-moment)*math.pi/40
            radius=.7-(35-moment)*.008
            x,z=radius*math.cos(angle),radius*math.sin(angle)
            y=.15+(35-moment)*.035
            lines.append(f'particle minecraft:dust{{color:[1.0,0.84,0.35],scale:0.7}} ~{x:.3f} ~{y:.3f} ~{z:.3f} 0 0 0 0 1 normal @s')
        lines.append('particle minecraft:end_rod ~ ~0.8 ~ 0.18 0.4 0.18 0.015 3 normal @s')
        write(rel+'.mcfunction',lines)
        animate.append(f'execute if score @s rpg_pr_time matches {moment} run function rpg:{rel}')
    animate.append('execute if score @s rpg_pr_time matches 0 run function rpg:prayer/claim')
    write('prayer/animate.mcfunction',animate)
    pool=[msg(text('+------ 恩赐名录 · 固定概率 ------+','#D4AF37',True))]
    md=['# 圣所祷告 · 奖池与概率','',f'每次消耗 **{cost} 枚数据包货币**，播放约 {ticks/20:g} 秒光环动画后获得一项恩赐。',
        '','入口：玩家面板 → 圣所祷告，或 `/function rpg:prayer/menu`；普通玩家可用 `/trigger rpg_pray set 1`。',
        '','## 规则','',
        '- 只接受带 `currency_tag:1b` 的货币；普通粗金无效。现有定制掉落中的货币已补标记，名称及整段说明完全匹配的旧币会在打开菜单或祷告时迁移。',
        '- 扣费前检查货币和背包空格。奖品在扣费当刻确定，动画期间不接受第二次扣费。',
        '- 断线、死亡、旁观或背包后来变满：奖品记在个人待领记录中，重连继续动画或从菜单免费领取；不会重新随机。',
        '- 每次固定概率、无保底、可重复获得；数量不改变该条目的中奖概率。至少空出一个主背包格。',
        '- 所有奖品完整复用数据包规范物品，保留技能、附魔、纹理和文本；旧约、新约、真名见证、剧情线索和测试物不入池。',
        '', '## 类别占比','', '| 类别 | 权重 | 单次总概率 |','|---|---:|---:|']
    for g in groups.values():
        weight=sum(e['weight'] for e in entries if e['group']==g['id'])
        md.append(f'| {g["name"]} | {weight} | {percent(weight)} |')
    md+=['','## 全部奖品（无条件单次概率）','','| 类别 | 奖品 | 数量 | 权重 | 实际概率 | 随机区间 |','|---|---|---:|---:|---:|---|']
    for e,lo,hi in bounds:
        group=groups[e['group']]
        md.append(f'| {group["name"]} | {e["name"]} | {e["count"]} | {e["weight"]} | {percent(e["weight"])} | {lo}–{hi} |')
        pool.append(msg(text(f'[{group["name"]}] ',group['color'],True),text(e['name'],group['color']),f' ×{e["count"]}  ·  {percent(e["weight"])}'))
    md+=['','权重合计 **10000**，实际概率合计 **100.00%**。以均匀整数 `1..10000` 抽取，所有区间互斥且连续；没有隐藏二次抽选。',
         '', '## 货币来源与调试','',
         '- 既有僵尸、尸壳、骷髅、僵尸村民定制战利品表及试炼/不祥试炼奖励；无尽「遗珍」现也使用数据包货币与定制物资。',
         '- `/function rpg:prayer/debug/coins`：只给执行玩家 64 枚测试货币。',
         '- `/function rpg:prayer/start`：正常付费祷告；`/function rpg:prayer/claim`：领取已付费奖品。',
         '- `/function rpg:prayer/pool`：游戏内完整概率表。',
         '', '## 工程来源','',
         '`_prayer_pool.json` 是费用、动画时长与权重的唯一配置；`_tools/add_prayer.py` 生成玩法、此文档及图鉴表格。修改后需重建、验证并 `/reload`，不要只手改本表。','']
    pool.append(msg(text('[返回祷告]','#FFD85A',True,'/trigger rpg_pray set 1')))
    write('prayer/pool.mcfunction',pool)
    (ROOT/'PRAYER-POOL.md').write_text('\n'.join(md),encoding='utf-8')
    (DP/'data/rpg/prayer_pool.json').write_text(json.dumps(CFG,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'prayer: {len(entries)} canonical rewards / 10000 weight / {cost} coins / {ticks} tick animation / {currency_changes} currency tables repaired')


if __name__=='__main__': main()
