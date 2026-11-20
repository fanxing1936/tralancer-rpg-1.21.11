# 补满本段血量，并补上副手的死亡保护（上一段的那件可能刚被吃掉）。
attribute @s minecraft:max_health base set 1200
data merge entity @s {Health:1200f}
scoreboard players set @s rpg_mk_h 1200
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty"]
