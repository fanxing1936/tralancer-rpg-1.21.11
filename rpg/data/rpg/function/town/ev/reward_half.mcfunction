# 奖励（as 参与者）：#kind 1 驱魔 2 战斗 3 世界观
scoreboard players operation #t rpg_tl = #run rpg_te
function rpg:town/life/rep_add {n:8}
function rpg:events/bt/town_event
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
