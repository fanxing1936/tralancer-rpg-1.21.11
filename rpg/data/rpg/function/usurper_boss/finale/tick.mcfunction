scoreboard players add @s rpg_ub_c 1
execute if score @s rpg_ub_c matches 1..90 run particle minecraft:end_rod ~ ~1.5 ~ 0.5 1 0.5 0.05 3
execute if score @s rpg_ub_c matches 20 if entity @s[tag=rpg.usb.s2] run function rpg:usurper_boss/finale/crown
execute if score @s rpg_ub_c matches 21 run function rpg:usurper_boss/finale/shards_fly
execute if score @s rpg_ub_c matches 40 run function rpg:usurper_boss/finale/return
execute if score @s rpg_ub_c matches 118.. run function rpg:usurper_boss/victory
