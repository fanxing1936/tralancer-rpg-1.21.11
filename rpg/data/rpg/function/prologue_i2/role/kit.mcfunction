# 发角色装备（as 玩家）：清空、武器、护甲（皮甲底，equippable 套 rpg:prologue_<角色> 的盔甲层、腿甲层与翅膀层）、副手死亡保护、生命 +20
clear @s
attribute @s minecraft:max_health modifier remove rpg:prologue/hp
attribute @s minecraft:max_health modifier add rpg:prologue/hp 20 add_value
execute if score @s rpg_pr_role matches 1 run function rpg:prologue_i2/role/kit_1
execute if score @s rpg_pr_role matches 2 run function rpg:prologue_i2/role/kit_2
execute if score @s rpg_pr_role matches 3 run function rpg:prologue_i2/role/kit_3
execute if score @s rpg_pr_role matches 4 run function rpg:prologue_i2/role/kit_4
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]
effect give @s minecraft:instant_health 1 9 true
effect give @s minecraft:saturation 1 9 true
scoreboard players set @s rpg_pr_cd1 0
scoreboard players set @s rpg_pr_cd2 0
