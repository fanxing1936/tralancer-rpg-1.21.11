# 空缺者的显形与代价。
# 只有附近有人持圣器时才现形 —— 平时它和普通村民毫无分别。
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run effect give @s minecraft:glowing 2 0 true
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run particle sculk_soul ~ ~1.4 ~ 0.2 0.3 0.2 0.01 2

# 杀掉空缺者不算驱魔 —— 罪落在动手的人身上。
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s on attacker run scoreboard players add @s rpg_taint 6
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s on attacker run title @s actionbar ["",{"text":"你打碎的只是空壳","italic":true,"color":"dark_gray"}]
