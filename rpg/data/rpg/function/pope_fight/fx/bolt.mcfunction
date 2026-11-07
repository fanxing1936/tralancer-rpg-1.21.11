tp @s ^ ^ ^0.9
particle dust{color:[0.835f,0.588f,0.949f],scale:1.0} ~ ~ ~ 0.1 0.1 0.1 0 2 normal
execute positioned ~ ~-0.6 ~ if entity @a[distance=..1.2,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/fx/bolt_hit
execute unless block ~ ~ ~ #minecraft:replaceable run function rpg:pope_fight/fx/bolt_burst
