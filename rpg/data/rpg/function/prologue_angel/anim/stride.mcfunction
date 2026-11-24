# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_pran_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_pran run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_pran run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_pran = #x rpg_pran
scoreboard players operation #dx rpg_pran -= @s rpg_pran_x
scoreboard players operation #dz rpg_pran = #z rpg_pran
scoreboard players operation #dz rpg_pran -= @s rpg_pran_z
scoreboard players operation @s rpg_pran_x = #x rpg_pran
scoreboard players operation @s rpg_pran_z = #z rpg_pran
scoreboard players operation #dx rpg_pran *= #dx rpg_pran
scoreboard players operation #dz rpg_pran *= #dz rpg_pran
scoreboard players operation #dx rpg_pran += #dz rpg_pran
execute store success score @s rpg_pran_mv if score #dx rpg_pran matches 64..
