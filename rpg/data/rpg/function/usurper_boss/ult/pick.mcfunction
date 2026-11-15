execute if score #ult rpg_ub matches 1 run tag @s add rpg.usb.u1
execute if score #ult rpg_ub matches 2 run tag @s add rpg.usb.u2
scoreboard players set @s rpg_ub_c 0
# 两招轮流：血线 1 / 时钟到点且上一招是 2 → 第一招；否则第二招
execute if score #ult rpg_ub matches 9 if entity @s[tag=rpg.usb.last1] run scoreboard players set #ult rpg_ub 2
execute if score #ult rpg_ub matches 9 run scoreboard players set #ult rpg_ub 1
execute if score @s rpg_ub matches 1 if score #ult rpg_ub matches 1 run function rpg:usurper_boss/ult/ring
execute if score @s rpg_ub matches 1 if score #ult rpg_ub matches 2 run function rpg:usurper_boss/ult/key
execute if score @s rpg_ub matches 2 if score #ult rpg_ub matches 1 run function rpg:usurper_boss/ult/overcharge
execute if score @s rpg_ub matches 2 if score #ult rpg_ub matches 2 run function rpg:usurper_boss/ult/judgment
execute if score #ult rpg_ub matches 1 run tag @s add rpg.usb.last1
execute if score #ult rpg_ub matches 2 run tag @s remove rpg.usb.last1
