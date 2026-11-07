# 开一场：记下战场中心。
kill @e[type=minecraft:marker,tag=rpg.pf.center]
summon minecraft:marker ~ ~ ~ {Tags:["rpg.pf.center"]}
scoreboard players set #t rpg_pf 0
scoreboard players set #s rpg_pf 0
scoreboard players set #e rpg_pf 0
bossbar set minecraft:pope players @a[distance=..48]
bossbar set minecraft:pope color pink
bossbar set minecraft:pope visible true
