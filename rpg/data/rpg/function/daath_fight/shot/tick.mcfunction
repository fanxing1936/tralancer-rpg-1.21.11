# 飞行的箭（as/at 箭）：每刻 1.2 格，分两步查
scoreboard players remove @s rpg_dt_life 1
execute if score @s rpg_dt_life matches ..0 run return run kill @s
execute positioned ^ ^ ^0.6 if entity @a[tag=rpg.dt.in,distance=..1.9,gamemode=!spectator,gamemode=!creative] positioned ~ ~-0.9 ~ if entity @a[tag=rpg.dt.in,distance=..1.15] run return run function rpg:daath_fight/shot/land
execute positioned ^ ^ ^1.2 positioned ~ ~-0.9 ~ if entity @a[tag=rpg.dt.in,distance=..1.15,gamemode=!spectator,gamemode=!creative] run return run function rpg:daath_fight/shot/land
tp @s ^ ^ ^1.2
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~ ~ 0.05 0.05 0.05 0 1
