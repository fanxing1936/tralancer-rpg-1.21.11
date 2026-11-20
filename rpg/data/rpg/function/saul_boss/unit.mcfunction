# 载体每刻（as/at 载体）。
execute if entity @s[tag=rpg.slb.end] run return run function rpg:saul_boss/finale/tick
execute if entity @s[tag=!rpg.slb.hp] run return run function rpg:saul_boss/hp_init
# 保险：离场地中心太远或掉到下面（冲出空岛边缘）就拉回中心；千刀里藏到地下的那段除外
execute unless entity @s[tag=rpg.slb.hidden] at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] unless entity @s[distance=..36] run function rpg:saul_boss/safety/back
execute unless entity @s[tag=rpg.slb.hidden] at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] positioned ~-48 ~-80 ~-48 if entity @s[dx=96,dy=72,dz=96] run function rpg:saul_boss/safety/back
scoreboard players operation #m rpg_sl = #tick rpg_sl
scoreboard players set #k rpg_sl 4
scoreboard players operation #m rpg_sl %= #k rpg_sl
execute if score #m rpg_sl matches 0 run function rpg:saul_boss/read_hp
execute if score @s rpg_sl matches 1 if score @s rpg_sl_h matches ..1 run return run function rpg:saul_boss/stage/end1
execute if score @s rpg_sl matches 2 if score @s rpg_sl_h matches ..1 run return run function rpg:saul_boss/stage/end2
execute if entity @s[tag=rpg.slb.morph] run return run function rpg:saul_boss/morph/tick
execute if score @s rpg_sl matches 2 run function rpg:saul_boss/s2/aura
scoreboard players add @s rpg_sl_c 1
execute if score @s rpg_sl_sk matches 1.. run function rpg:saul_boss/sk/tick
execute if score @s rpg_sl_busy matches 1.. run return run scoreboard players remove @s rpg_sl_busy 1
function rpg:saul_boss/schedule
