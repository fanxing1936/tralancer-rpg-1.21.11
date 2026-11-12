tp @s ^ ^ ^0.9
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.2} ~ ~ ~ 0.05 0.05 0.05 0 1
execute unless block ~ ~ ~ #minecraft:replaceable run return run function rpg:lucifer_fight/dart/pop
execute positioned ~ ~-0.9 ~ if entity @a[distance=..1,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/dart/strike
