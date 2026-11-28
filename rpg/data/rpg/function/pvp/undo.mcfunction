# 补回刚才挨的那一下（as 挨打的人）：瞬间治疗一次补 4 点
execute store result score #now rpg_pv_n run data get entity @s Health 10
scoreboard players operation #lost rpg_pv_n = @s rpg_pv_hp
scoreboard players operation #lost rpg_pv_n -= #now rpg_pv_n
execute if score #lost rpg_pv_n matches 1.. run function rpg:pvp/heal
