# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_bls_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_bls run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_bls run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_bls = #x rpg_bls
scoreboard players operation #dx rpg_bls -= @s rpg_bls_x
scoreboard players operation #dz rpg_bls = #z rpg_bls
scoreboard players operation #dz rpg_bls -= @s rpg_bls_z
scoreboard players operation @s rpg_bls_x = #x rpg_bls
scoreboard players operation @s rpg_bls_z = #z rpg_bls
scoreboard players operation #dx rpg_bls *= #dx rpg_bls
scoreboard players operation #dz rpg_bls *= #dz rpg_bls
scoreboard players operation #dx rpg_bls += #dz rpg_bls
execute store success score @s rpg_bls_mv if score #dx rpg_bls matches 64..
