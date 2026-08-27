"""Exhaustive pool and canonical reward / ritual supply contracts."""
import json
from pathlib import Path
import re
import sys
from rpg_catalogue import catalogue, give, resolve, max_stack

ROOT=Path(__file__).resolve().parent.parent
DP=Path(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else ROOT/'rpg').resolve()
F=DP/'data/rpg/function'
pool=json.loads((ROOT/'_prayer_pool.json').read_text(encoding='utf-8'))
supply=json.loads((ROOT/'_endless_supplies.json').read_text(encoding='utf-8'))
items=catalogue(DP)
def source(path):return (F/(path+'.mcfunction')).read_text(encoding='utf-8')
def require(test,msg):
    if not test:raise AssertionError(msg)

require(sum(e['weight'] for e in pool['entries'])==pool['total_weight']==10000,'pool total')
hits=[0]*10001
select=source('prayer/select')
for lo,hi,index in re.findall(r'matches (\d+)\.\.(\d+) run scoreboard players set @s rpg_pr_pending (\d+)',select):
    lo,hi,index=map(int,(lo,hi,index))
    require(hi-lo+1==pool['entries'][index-1]['weight'],'weight mismatch')
    for roll in range(lo,hi+1):hits[roll]+=1
require(all(n==1 for n in hits[1:]),'every draw must map exactly once')
for e in pool['entries']:
    body=source('prayer/reward/'+e['key'])
    require(give(items,e['name'],e['count']) in body,'canonical prize '+e['name'])
    record=resolve(items,e['name'])
    require(e['count']<=max_stack(record['id'],record['block']),'prize exceeds one slot')
    require(e['name'] not in ('新约','旧约'),'unique story prize in pool')
    require('rpg_pr_pending 0' in body,'claim does not settle pending')
start=source('prayer/start')
ordered=['rpg_pr_time matches','rpg_pr_pending matches','function rpg:prayer/currency','function rpg:prayer/space','store result score @s rpg_pr_paid','function rpg:prayer/select','rpg_pr_time 40']
require([start.index(x) for x in ordered]==sorted(start.index(x) for x in ordered),'payment checks/order')
require('minecraft:custom_data~{currency_tag:1b}' in start,'accepts plain raw gold')
require('function rpg:prayer/claim' in source('prayer/animate'),'animation has no settlement')
require('rpg_pr_time matches 1..' in source('prayer/claim'),'claim bypasses animation')
require('function rpg:prayer/error/pending' in source('prayer/claim'),'full inventory loses reward')
require(source('prayer/space').count('Slot:')==36,'must inspect all main inventory slots')
for p in (F/'prayer').rglob('*.mcfunction'):
    require('actionbar' not in p.read_text(encoding='utf-8'),'prayer overwrites HUD')
request=source('endless/supply/request')
for token in ('tag=rpg.end.member.current','rpg_end_id =','rpg_end_kit_id =','rpg_end_kit_floor =','rpg_end_state matches 1','%= #five','gamemode=!spectator','Health:0.0f','rpg_end_kit_lord = #supply_lord'):
    require(token in request,'supply ownership/state missing '+token)
boss=source('endless/boss/dispatch')
require(boss.index('function rpg:endless/supply/request')<boss.index('function rpg:endless/boss/1'),'supply must precede boss')
for lord in range(1,8):
    body=source(f'endless/supply/kit{lord}')
    require(f'rpg:endless/supply/kit{lord}' in request,'missing lord kit')
    require(body.count('Slot:')==36,'supply inventory check')
    require(body.index('rpg_end_free < @s rpg_end_need')<body.index('run give @s'),'supply gives before checking room')
    require(body.index('run give @s')<body.index('rpg_end_kit_floor ='),'stamp before delivery')
    for name,count in supply['boss_kit']:
        require(give(items,name,count) in body,'missing minimum '+name)
    require('rpg_inq_' not in body,'kit bypasses investigation')
for index,tier in enumerate(supply['relic_tiers'],1):
    for name,count in tier['items']:
        require(give(items,name,count) in source(f'endless/reward/loot/{index}'),'noncanonical relic')
if '--docs' in sys.argv:
    md=(ROOT/'PRAYER-POOL.md').read_text(encoding='utf-8')
    html=(ROOT/'TRALANCER-RPG-图鉴.html').read_text(encoding='utf-8')
    for e in pool['entries']:
        for text in (md,html):
            require(e['name'] in text,'undocumented prize')
            require(f"{e['weight']/100:.2f}%" in text,'undocumented odds')
    require('id="s18"' in html and 'rpg_end_supply set 1' in html,'guide entry missing')
print('PRAYER + SUPPLY: PASS (10,000 draws / 27 canonical prizes / 7 protected ritual kits)')
