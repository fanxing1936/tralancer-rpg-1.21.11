execute if entity @s[tag=rpg.legacy.bubble] run particle minecraft:dust_color_transition{from_color:[0.0,0.7,1.0],to_color:[0.56,0.97,1.0],scale:1.2} ~ ~ ~ 0.12 0.12 0.12 0.02 5 force
execute if entity @s[tag=rpg.legacy.burn] run particle minecraft:flame ~ ~ ~ 0.12 0.12 0.12 0.02 5 force
execute if entity @s[tag=rpg.legacy.hunter] run particle minecraft:dust_color_transition{from_color:[0.69,0.0,0.34],to_color:[0.26,0.64,0.93],scale:1.2} ~ ~ ~ 0.12 0.12 0.12 0.02 5 force
execute if entity @s[tag=rpg.legacy.bubble] if entity @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/bubble_hit
execute if entity @s[tag=rpg.legacy.burn] if entity @e[distance=..1.2,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/burn_hit
execute if entity @s[tag=rpg.legacy.hunter] if entity @e[distance=..1.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows,limit=1] run function rpg:item/legacy/hunter_hit
execute if entity @s[nbt={inGround:1b}] run return run kill @s
scoreboard players add @s rpg_proj_t 1
execute if score @s rpg_proj_t matches 200.. run kill @s
