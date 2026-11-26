# 奖励（as 玩家，已回到原处）
execute unless score @s rpg_dt_win matches 2.. run loot give @s loot rpg:daath/shard
execute if score @s rpg_dt_win matches 2.. unless score @s rpg_dt_rd = #day rpg_sef run loot give @s loot rpg:forge/item/soul
execute if score @s rpg_dt_win matches 2.. unless score @s rpg_dt_rd = #day rpg_sef run loot give @s loot rpg:forge/item/soul
scoreboard players operation @s rpg_dt_rd = #day rpg_sef
