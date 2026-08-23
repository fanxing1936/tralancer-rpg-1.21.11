# 一个目标的份。回血落在施术者身上 —— 收割是拿命换命。
damage @s 8 minecraft:magic by @a[tag=rpg.pact.cast,limit=1,sort=nearest]
effect give @s minecraft:wither 4 0 true
particle soul ~ ~1 ~ 0.2 0.4 0.2 0.06 12
execute as @a[tag=rpg.pact.cast,limit=1,sort=nearest] run effect give @s minecraft:instant_health 1 0 true
