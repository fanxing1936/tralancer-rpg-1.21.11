# 飞行一刻（as、at 弹体）。
tp @s ^ ^ ^0.7
execute if entity @s[tag=rpg.pf.quick] run tp @s ^ ^ ^0.5
execute if score #go rpg_pf matches 1 run function rpg:pope_fight/fx/frame_orb
particle end_rod ~ ~ ~ 0.05 0.05 0.05 0.01 1 normal
execute positioned ~ ~-0.6 ~ if entity @a[distance=..1.2,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/fx/blast_hit
execute unless block ~ ~ ~ #minecraft:replaceable run function rpg:pope_fight/fx/blast_burst
