scoreboard players remove @s rpg_ub_x 1
scoreboard players operation #m rpg_ub = @s rpg_ub_x
scoreboard players set #k rpg_ub 4
scoreboard players operation #m rpg_ub %= #k rpg_ub
# 王冠暗下，裂纹一闪一闪
execute if score #m rpg_ub matches 0 run execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[3945512]}
execute if score #m rpg_ub matches 2 run execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[9073216]}
scoreboard players operation #m rpg_ub = @s rpg_ub_x
scoreboard players set #k rpg_ub 8
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 at @s run function rpg:usurper_boss/weak/mote
execute if score @s rpg_ub_x matches ..0 run function rpg:usurper_boss/weak/end
