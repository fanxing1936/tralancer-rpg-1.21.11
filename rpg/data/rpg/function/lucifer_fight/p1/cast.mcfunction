# 五招掷一招，撞上一招就顺延。
execute store result score #pick rpg_l2_v run random value 1..5
execute if score #pick rpg_l2_v = @s rpg_dm_last run scoreboard players add #pick rpg_l2_v 1
execute if score #pick rpg_l2_v matches 6.. run scoreboard players set #pick rpg_l2_v 1
scoreboard players operation @s rpg_dm_last = #pick rpg_l2_v
function rpg:lucifer_fight/p1/begin
scoreboard players set @s rpg_dm_cd 30
execute if score #pick rpg_l2_v matches 1 run return run function rpg:lucifer_fight/p1/sin/start
execute if score #pick rpg_l2_v matches 2 run return run function rpg:lucifer_fight/p1/spear/start
execute if score #pick rpg_l2_v matches 3 run return run function rpg:lucifer_fight/p1/high/start
execute if score #pick rpg_l2_v matches 4 run return run function rpg:lucifer_fight/p1/fall/start
execute if score #pick rpg_l2_v matches 5 run return run function rpg:lucifer_fight/p1/throne/start
