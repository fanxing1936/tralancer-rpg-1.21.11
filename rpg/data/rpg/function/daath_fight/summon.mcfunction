# 管理员：立刻进场（as/at 玩家），不看阶位与冷却
execute if score @s rpg_dt matches 1.. run return run function rpg:daath_fight/clear
scoreboard players set #slot rpg_dt 0
execute if score #slot rpg_dt matches 0 unless score #b1 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 1
execute if score #slot rpg_dt matches 0 unless score #b2 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 2
execute if score #slot rpg_dt matches 0 unless score #b3 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 3
execute if score #slot rpg_dt matches 0 unless score #b4 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 4
execute if score #slot rpg_dt matches 0 unless score #b5 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 5
execute if score #slot rpg_dt matches 0 unless score #b6 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 6
execute if score #slot rpg_dt matches 0 unless score #b7 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 7
execute if score #slot rpg_dt matches 0 unless score #b8 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 8
execute if score #slot rpg_dt matches 0 unless score #b9 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 9
execute if score #slot rpg_dt matches 0 unless score #b10 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 10
execute if score #slot rpg_dt matches 0 unless score #b11 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 11
execute if score #slot rpg_dt matches 0 unless score #b12 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 12
execute if score #slot rpg_dt matches 0 unless score #b13 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 13
execute if score #slot rpg_dt matches 0 unless score #b14 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 14
execute if score #slot rpg_dt matches 0 unless score #b15 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 15
execute if score #slot rpg_dt matches 0 unless score #b16 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 16
execute if score #slot rpg_dt matches 1.. run function rpg:daath_fight/begin
