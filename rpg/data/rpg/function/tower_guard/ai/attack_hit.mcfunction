# 戟刃落下：前方一人受击。
tag @s add rpg.tg.self
damage @e[tag=rpg.unit.f,distance=..2.2,sort=nearest,limit=1] 8 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.tg.self,limit=1]
tag @s remove rpg.tg.self
