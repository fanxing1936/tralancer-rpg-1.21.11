# 权柄线（as 线）：它的圣卫倒下了就断
scoreboard players operation #id rpg_ub = @s rpg_ub_id
scoreboard players set #n rpg_ub 0
execute as @e[tag=rpg.usb.guard] if score @s rpg_ub_id = #id rpg_ub run scoreboard players set #n rpg_ub 1
execute if score #n rpg_ub matches 0 at @s run function rpg:usurper_boss/auth/snap
