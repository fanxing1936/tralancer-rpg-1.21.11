# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_dtm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_dtm run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_dtm run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_dtm = #x rpg_dtm
scoreboard players operation #dx rpg_dtm -= @s rpg_dtm_x
scoreboard players operation #dz rpg_dtm = #z rpg_dtm
scoreboard players operation #dz rpg_dtm -= @s rpg_dtm_z
scoreboard players operation @s rpg_dtm_x = #x rpg_dtm
scoreboard players operation @s rpg_dtm_z = #z rpg_dtm
scoreboard players operation #dx rpg_dtm *= #dx rpg_dtm
scoreboard players operation #dz rpg_dtm *= #dz rpg_dtm
scoreboard players operation #dx rpg_dtm += #dz rpg_dtm
execute store success score @s rpg_dtm_mv if score #dx rpg_dtm matches 64..
