# 载体每刻（as/at 载体）。
execute if entity @s[tag=rpg.usb.end] run return run function rpg:usurper_boss/finale/tick
execute if entity @s[tag=!rpg.usb.hp] run return run function rpg:usurper_boss/hp_init
scoreboard players operation #m rpg_ub = #tick rpg_ub
scoreboard players set #k rpg_ub 4
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 run function rpg:usurper_boss/read_hp
execute if score @s rpg_ub matches 1 if score @s rpg_ub_h matches ..1 run return run function rpg:usurper_boss/stage/end1
execute if score @s rpg_ub matches 2 if score @s rpg_ub_h matches ..1 run return run function rpg:usurper_boss/stage/end2
execute if entity @s[tag=rpg.usb.morph] run return run function rpg:usurper_boss/morph/tick
scoreboard players add @s rpg_ub_c 1
execute if score @s rpg_ub_sk matches 1.. run function rpg:usurper_boss/sk/tick
execute if score @s rpg_ub matches 1 if score @s rpg_ub_busy matches ..0 run function rpg:usurper_boss/wave/check
execute if score @s rpg_ub matches 2 run function rpg:usurper_boss/s2/tick
execute if score @s rpg_ub_busy matches 1.. run return run scoreboard players remove @s rpg_ub_busy 1
function rpg:usurper_boss/schedule
