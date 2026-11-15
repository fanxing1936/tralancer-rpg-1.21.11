# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_bll_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_bll run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_bll run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_bll = #x rpg_bll
scoreboard players operation #dx rpg_bll -= @s rpg_bll_x
scoreboard players operation #dz rpg_bll = #z rpg_bll
scoreboard players operation #dz rpg_bll -= @s rpg_bll_z
scoreboard players operation @s rpg_bll_x = #x rpg_bll
scoreboard players operation @s rpg_bll_z = #z rpg_bll
scoreboard players operation #dx rpg_bll *= #dx rpg_bll
scoreboard players operation #dz rpg_bll *= #dz rpg_bll
scoreboard players operation #dx rpg_bll += #dz rpg_bll
execute store success score @s rpg_bll_mv if score #dx rpg_bll matches 64..
