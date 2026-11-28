# F（as/at 玩家）：武器换回主手、死亡保护放回副手
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]
execute if predicate rpg:prologue_i2/sneaking run return run function rpg:prologue_i2/role/ult
function rpg:prologue_i2/role/skill
