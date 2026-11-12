scoreboard players remove @s rpg_l2_t 1
execute if score @s rpg_l2_t matches ..0 run return run kill @s
execute if entity @s[type=minecraft:block_display,tag=rpg.lu2f.vine] run function rpg:lucifer_fight/vine/life
execute if entity @s[tag=rpg.lu2f.anim] run function rpg:lucifer_fight/fx/anim
