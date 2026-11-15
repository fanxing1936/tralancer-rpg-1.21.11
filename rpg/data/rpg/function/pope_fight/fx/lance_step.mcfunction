execute positioned ~ ~-1 ~ as @e[tag=rpg.unit.f,distance=..1.6] run damage @s 14 minecraft:indirect_magic by @e[type=minecraft:vindicator,tag=rpg.pf.boss,limit=1]
particle end_rod ~ ~ ~ 0.15 0.15 0.15 0.02 1 normal
scoreboard players add #d rpg_pf 1
execute if score #d rpg_pf matches ..19 positioned ^ ^ ^2 run function rpg:pope_fight/fx/lance_step
