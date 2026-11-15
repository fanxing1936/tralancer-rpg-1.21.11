# 一道弦落下（as/at 弦的标记，朝弦的方向）：变粗变亮，弦上 1 格内 12
execute positioned ^ ^0.6 ^-15 run function rpg:jacques_boss/harp/hit
scoreboard players operation #i rpg_jq = @s rpg_jq_id
execute as @e[tag=rpg.jqb.strv] if score @s rpg_jq_id = #i rpg_jq run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{scale:[0.7f,0.3f,30f]}}
execute as @e[tag=rpg.jqb.strv] if score @s rpg_jq_id = #i rpg_jq run data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value 16773832
particle minecraft:end_rod ~ ~0.3 ~ 0 0 0 0.12 12
execute positioned ^ ^ ^-15 run function rpg:jacques_boss/harp/fall_fx
execute if score #i rpg_jq matches 0 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.5
execute if score #i rpg_jq matches 1 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.56
execute if score #i rpg_jq matches 2 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.63
execute if score #i rpg_jq matches 3 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.67
execute if score #i rpg_jq matches 4 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.75
execute if score #i rpg_jq matches 5 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.84
execute if score #i rpg_jq matches 6 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 0.94
execute if score #i rpg_jq matches 7 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 1.0
execute if score #i rpg_jq matches 8 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 1.12
execute if score #i rpg_jq matches 9 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 1.26
execute if score #i rpg_jq matches 10 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 1.33
execute if score #i rpg_jq matches 11 run playsound minecraft:block.note_block.harp hostile @a[distance=..32] ~ ~ ~ 1.2 1.5
kill @s

