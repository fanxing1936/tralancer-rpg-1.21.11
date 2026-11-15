# 载体每刻（as/at 载体）。
execute if entity @s[tag=rpg.jqb.end] run return run function rpg:jacques_boss/finale/tick
execute if entity @s[tag=!rpg.jqb.hp] run return run function rpg:jacques_boss/hp_init
scoreboard players operation #m rpg_jq = #tick rpg_jq
scoreboard players set #k rpg_jq 4
scoreboard players operation #m rpg_jq %= #k rpg_jq
execute if score #m rpg_jq matches 0 run function rpg:jacques_boss/read_hp
execute if score @s rpg_jq matches 1 if score @s rpg_jq_h matches ..1 run return run function rpg:jacques_boss/stage/end1
execute if score @s rpg_jq matches 2 if score @s rpg_jq_h matches ..1 run return run function rpg:jacques_boss/stage/end2
execute if entity @s[tag=rpg.jqb.morph] run return run function rpg:jacques_boss/morph/tick
execute if score @s rpg_jq matches 2 run function rpg:jacques_boss/s2/burn
scoreboard players add @s rpg_jq_c 1
execute if score @s rpg_jq_sk matches 1.. run function rpg:jacques_boss/sk/tick
execute if score @s rpg_jq_busy matches 1.. run return run scoreboard players remove @s rpg_jq_busy 1
function rpg:jacques_boss/schedule
