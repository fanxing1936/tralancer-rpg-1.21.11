# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prbz_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prbz run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prbz run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prbz = #x rpg_prbz
scoreboard players operation #dx rpg_prbz -= @s rpg_prbz_x
scoreboard players operation #dz rpg_prbz = #z rpg_prbz
scoreboard players operation #dz rpg_prbz -= @s rpg_prbz_z
scoreboard players operation @s rpg_prbz_x = #x rpg_prbz
scoreboard players operation @s rpg_prbz_z = #z rpg_prbz
scoreboard players operation #dx rpg_prbz *= #dx rpg_prbz
scoreboard players operation #dz rpg_prbz *= #dz rpg_prbz
scoreboard players operation #dx rpg_prbz += #dz rpg_prbz
execute store success score @s rpg_prbz_mv if score #dx rpg_prbz matches 64..
