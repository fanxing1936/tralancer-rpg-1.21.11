# 铺屏障前，站在圣坛脚下 2×2 里的人先托到坛顶，免得卡进方块
execute if score @s rpg_ub_t matches 16 as @e[type=minecraft:marker,tag=rpg.usb.altar] at @s as @e[tag=rpg.unit,dx=1,dy=1,dz=1] run tp @s ~1 ~2.05 ~1
execute if score @s rpg_ub_t matches 16 at @e[type=minecraft:marker,tag=rpg.usb.altar] run fill ~ ~ ~ ~1 ~1 ~1 minecraft:barrier replace minecraft:air
execute if score @s rpg_ub_t matches 66 run function rpg:prime_enchanter/anim/enter/overcharge
execute if score @s rpg_ub_t matches 28 run function rpg:usurper_boss/over/warn
execute if score @s rpg_ub_t matches 40 run function rpg:usurper_boss/over/strike0
execute if score @s rpg_ub_t matches 53 run function rpg:usurper_boss/over/warn
execute if score @s rpg_ub_t matches 65 run function rpg:usurper_boss/over/strike1
execute if score @s rpg_ub_t matches 78 run function rpg:usurper_boss/over/warn
execute if score @s rpg_ub_t matches 90 run function rpg:usurper_boss/over/strike2
execute if score @s rpg_ub_t matches 103 run function rpg:usurper_boss/over/warn
execute if score @s rpg_ub_t matches 115 run function rpg:usurper_boss/over/strike3
execute if score @s rpg_ub_t matches 120 run function rpg:usurper_boss/over/end
execute if score @s rpg_ub_t matches 140.. run function rpg:usurper_boss/sk/end
