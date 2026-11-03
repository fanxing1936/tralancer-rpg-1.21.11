# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_lv_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_lv run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_lv run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_lv = #x rpg_lv
scoreboard players operation #dx rpg_lv -= @s rpg_lv_x
scoreboard players operation #dz rpg_lv = #z rpg_lv
scoreboard players operation #dz rpg_lv -= @s rpg_lv_z
scoreboard players operation @s rpg_lv_x = #x rpg_lv
scoreboard players operation @s rpg_lv_z = #z rpg_lv
scoreboard players operation #dx rpg_lv *= #dx rpg_lv
scoreboard players operation #dz rpg_lv *= #dz rpg_lv
scoreboard players operation #dx rpg_lv += #dz rpg_lv
execute store success score @s rpg_lv_mv if score #dx rpg_lv matches 64..
