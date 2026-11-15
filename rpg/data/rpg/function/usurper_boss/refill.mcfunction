# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。
attribute @s minecraft:max_health base set 1000
data merge entity @s {Health:1000f}
scoreboard players set @s rpg_ub_h 1000
scoreboard players set @s rpg_ub_l 10000
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]
