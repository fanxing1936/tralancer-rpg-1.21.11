tag @s add rpg.fo.hit
attribute @s minecraft:armor modifier remove rpg:fo_rot
execute if score #lv rpg_fo matches 1 run attribute @s minecraft:armor modifier add rpg:fo_rot -4 add_value
execute if score #lv rpg_fo matches 2 run attribute @s minecraft:armor modifier add rpg:fo_rot -6 add_value
execute if score #lv rpg_fo matches 3 run attribute @s minecraft:armor modifier add rpg:fo_rot -8 add_value
tag @s add rpg.fo.timed
scoreboard players operation @s rpg_fo_end = #now rpg_fo
scoreboard players add @s rpg_fo_end 120
scoreboard players set #dmg rpg_fo 30
scoreboard players set #hm rpg_fo 10
function rpg:force/hit
