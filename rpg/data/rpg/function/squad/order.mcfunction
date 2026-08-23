# 指挥旗 —— 由 rpg:item/squad_order 在长按右键时触发。
# 不潜行：指着谁打谁。潜行：切换 跟随／驻守。
advancement revoke @s only rpg:item/squad_order
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t 10
execute unless score @s rpg_squad = @s rpg_squad run return run function rpg:squad/no_squad
scoreboard players operation #sq rpg_squad = @s rpg_squad
execute if predicate rpg:sneaking run return run function rpg:squad/stance
function rpg:squad/aim
