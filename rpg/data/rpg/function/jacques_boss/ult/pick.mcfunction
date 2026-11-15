execute if score #ult rpg_jq matches 1 run tag @s add rpg.jqb.u1
execute if score #ult rpg_jq matches 2 run tag @s add rpg.jqb.u2
scoreboard players set @s rpg_jq_c 0
# 两招轮流：血线 1 / 时钟到点且上一招是 2 → 第一招；否则第二招
execute if score #ult rpg_jq matches 9 if entity @s[tag=rpg.jqb.last1] run scoreboard players set #ult rpg_jq 2
execute if score #ult rpg_jq matches 9 run scoreboard players set #ult rpg_jq 1
execute if score @s rpg_jq matches 1 if score #ult rpg_jq matches 1 run function rpg:jacques_boss/ult/cross
execute if score @s rpg_jq matches 1 if score #ult rpg_jq matches 2 run function rpg:jacques_boss/ult/harp
execute if score @s rpg_jq matches 2 if score #ult rpg_jq matches 1 run function rpg:jacques_boss/ult/stakes
execute if score @s rpg_jq matches 2 if score #ult rpg_jq matches 2 run function rpg:jacques_boss/ult/last
execute if score #ult rpg_jq matches 1 run tag @s add rpg.jqb.last1
execute if score #ult rpg_jq matches 2 run tag @s remove rpg.jqb.last1
# 二阶段：大卫的幽灵甩出石子
execute if score @s rpg_jq matches 2 run function rpg:jacques_boss/david/throw
