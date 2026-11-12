# 水平初速按落点距离算：空中约 26 刻，横向阻力 0.91，总位移约为初速的 10.15 倍。
scoreboard players set @s rpg_l2_v 0
execute store result score #bx rpg_l2_v run data get entity @s Pos[0] 100
execute store result score #bz rpg_l2_v run data get entity @s Pos[2] 100
scoreboard players set #mx rpg_l2_v 0
scoreboard players set #mz rpg_l2_v 0
scoreboard players operation #mx rpg_l2_v = #bx rpg_l2_v
scoreboard players operation #mz rpg_l2_v = #bz rpg_l2_v
execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id store result score #mx rpg_l2_v run data get entity @s Pos[0] 100
execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id store result score #mz rpg_l2_v run data get entity @s Pos[2] 100
scoreboard players operation #mx rpg_l2_v -= #bx rpg_l2_v
scoreboard players operation #mz rpg_l2_v -= #bz rpg_l2_v
execute if score #mx rpg_l2_v matches 1401.. run scoreboard players set #mx rpg_l2_v 1400
execute if score #mx rpg_l2_v matches ..-1401 run scoreboard players set #mx rpg_l2_v -1400
execute if score #mz rpg_l2_v matches 1401.. run scoreboard players set #mz rpg_l2_v 1400
execute if score #mz rpg_l2_v matches ..-1401 run scoreboard players set #mz rpg_l2_v -1400
attribute @s minecraft:movement_speed modifier remove rpg:lu2f_hold
execute store result entity @s Motion[0] double 0.000985 run scoreboard players get #mx rpg_l2_v
execute store result entity @s Motion[2] double 0.000985 run scoreboard players get #mz rpg_l2_v
data modify entity @s Motion[1] set value 1.1d
function rpg:lucifer_fight/hold
playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..40] ~ ~ ~ 1.4 0.6
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 2 0.2 2 0.15 50
