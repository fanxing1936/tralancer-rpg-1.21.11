# 每秒：刷新血条观众；战场没人满 60 秒就判负清场。
scoreboard players set #s rpg_pf 0
bossbar set minecraft:pope players @a[distance=..48]
execute if entity @e[tag=rpg.unit.ns,distance=..40] run scoreboard players set #e rpg_pf 0
execute unless entity @e[tag=rpg.unit.ns,distance=..40] run scoreboard players add #e rpg_pf 1
execute if score #e rpg_pf matches 60.. run function rpg:pope_fight/fail
