scoreboard players add @s rpg_vt_t 1
scoreboard players operation #c rpg_vt = @s rpg_vt_id
execute as @e[type=minecraft:item_display,tag=rpg.vt.i,distance=..6] if score @s rpg_vt_id = #c rpg_vt run tag @s add rpg.vt.me
execute if score @s rpg_vt_m matches 0 run function rpg:vault/n
execute if score @s rpg_vt_m matches 1 run function rpg:vault/o
tag @e[tag=rpg.vt.me,distance=..8] remove rpg.vt.me
