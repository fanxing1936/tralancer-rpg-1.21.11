# 怠惰：站着不动 2 秒后抗性 I（美丽阶起 II）
execute store result score #x rpg_fo run data get entity @s Pos[0] 10
execute store result score #z rpg_fo run data get entity @s Pos[2] 10
execute unless score #x rpg_fo = @s rpg_fo_px run scoreboard players set @s rpg_fo_st 0
execute unless score #z rpg_fo = @s rpg_fo_pz run scoreboard players set @s rpg_fo_st 0
execute if score #x rpg_fo = @s rpg_fo_px if score #z rpg_fo = @s rpg_fo_pz run scoreboard players add @s rpg_fo_st 1
scoreboard players operation @s rpg_fo_px = #x rpg_fo
scoreboard players operation @s rpg_fo_pz = #z rpg_fo
execute unless score @s rpg_fo_st matches 2.. run return 0
execute unless score @s rpg_sef matches 5.. run effect give @s minecraft:resistance 2 0 true
execute if score @s rpg_sef matches 5.. run effect give @s minecraft:resistance 2 1 true
