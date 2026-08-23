# 指挥旗 —— 由 rpg:item/squad_order 在长按右键时触发。
# 不潜行：指着谁打谁。潜行：切换 跟随／驻守。
advancement revoke @s only rpg:item/squad_order
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t 10
execute unless score @s rpg_squad = @s rpg_squad run return run function rpg:squad/no_squad
scoreboard players operation #sq rpg_squad = @s rpg_squad
# 三个动作靠「潜行」与「副手空不空」分开。
#
# 配装原本走 player_interacted_with_entity（右键佣兵），但那个触发器只在
# 交互**被消费**时才响 —— 原版全部七个用例都是真的做成了一件事（刷、喂、
# 拴、修、引诱），而用剑右键一只尸壳在原版里什么都不做。所以那条路不响。
# 改走副手 + using_item，与包里其余主动物品同一条路。
execute if predicate rpg:sneaking if items entity @s weapon.offhand * run return run function rpg:squad/fire_near
execute if predicate rpg:sneaking run return run function rpg:squad/stance
execute if items entity @s weapon.offhand * run return run function rpg:squad/handover
function rpg:squad/aim
