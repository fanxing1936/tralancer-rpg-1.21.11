# 待雇 -> 在编。
tag @s remove rpg.sq.free
tag @s add rpg.squad
scoreboard players operation @s rpg_squad = #sq rpg_squad
scoreboard players set @s rpg_sq_mode 0
scoreboard players set @s rpg_sq_cd 0
data modify entity @s CustomName set value [{"text":"佣兵","color":"#8FA1B3"}]
particle happy_villager ~ ~1.6 ~ 0.3 0.3 0.3 0.1 30
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.03 16
