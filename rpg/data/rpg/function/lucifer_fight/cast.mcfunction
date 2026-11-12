# 五招掷一招，撞上一招就顺延（同一阶段的 sk1 规则）。
execute store result score #pick rpg_l2_v run random value 1..5
execute if score #pick rpg_l2_v = @s rpg_dm_last run scoreboard players add #pick rpg_l2_v 1
execute if score #pick rpg_l2_v matches 6.. run scoreboard players set #pick rpg_l2_v 1
scoreboard players operation @s rpg_dm_last = #pick rpg_l2_v
scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_t 0
scoreboard players operation @s rpg_l2_sk = #pick rpg_l2_v
function rpg:lucifer_fight/hold
scoreboard players set @s rpg_dm_cd 30
execute if score #pick rpg_l2_v matches 1 run return run function rpg:lucifer_fight/vine/start
execute if score #pick rpg_l2_v matches 2 run return run function rpg:lucifer_fight/fruit/start
execute if score #pick rpg_l2_v matches 3 run return run function rpg:lucifer_fight/tempt/start
execute if score #pick rpg_l2_v matches 4 run return run function rpg:lucifer_fight/fall/start
execute if score #pick rpg_l2_v matches 5 run return run function rpg:lucifer_fight/gaze/start
