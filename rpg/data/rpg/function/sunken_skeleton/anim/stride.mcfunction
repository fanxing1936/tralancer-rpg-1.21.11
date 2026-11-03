# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_sk_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_sk run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_sk run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_sk = #x rpg_sk
scoreboard players operation #dx rpg_sk -= @s rpg_sk_x
scoreboard players operation #dz rpg_sk = #z rpg_sk
scoreboard players operation #dz rpg_sk -= @s rpg_sk_z
scoreboard players operation @s rpg_sk_x = #x rpg_sk
scoreboard players operation @s rpg_sk_z = #z rpg_sk
scoreboard players operation #dx rpg_sk *= #dx rpg_sk
scoreboard players operation #dz rpg_sk *= #dz rpg_sk
scoreboard players operation #dx rpg_sk += #dz rpg_sk
execute store success score @s rpg_sk_mv if score #dx rpg_sk matches 64..
