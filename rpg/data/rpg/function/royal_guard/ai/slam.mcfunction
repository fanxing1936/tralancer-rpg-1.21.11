# 锤落地（at 落点）：一圈人受伤
tag @s add rpg.rg.self
execute as @e[tag=rpg.unit.f,distance=..2.6] run damage @s 9 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.rg.self,limit=1]
tag @s remove rpg.rg.self
playsound rpg:royal_guard.slam hostile @a[distance=..24] ~ ~ ~ 1 0.9
particle minecraft:dust_pillar{block_state:"minecraft:gold_block"} ~ ~0.1 ~ 1.2 0.1 1.2 0 30 normal
particle minecraft:end_rod ~ ~0.3 ~ 1 0.1 1 0.04 12 normal
