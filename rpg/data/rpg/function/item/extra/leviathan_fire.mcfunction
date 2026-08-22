# 满蓄。代价在这里结算：付不起就散掉，不硬扣。
execute store result score @s rpg_levi_hp run data get entity @s Health
execute if entity @s[scores={rpg_levi_hp=..10}] run playsound minecraft:entity.villager.no player @s
execute if entity @s[scores={rpg_levi_hp=..10}] at @s run particle smoke ~ ~1 ~ 0.3 0.3 0.3 0.01 12
execute if entity @s[scores={rpg_levi_hp=..10}] run scoreboard players reset @s rpg_levi_charge
execute if entity @s[scores={rpg_levi_hp=11..}] run function rpg:item/extra/leviathan_cast
