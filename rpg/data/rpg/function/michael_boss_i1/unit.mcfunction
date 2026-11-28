# 载体每刻（as/at 载体）。
execute if entity @s[tag=rpg.mkb.end] run return run function rpg:michael_boss_i1/finale/tick
execute if entity @s[tag=!rpg.mkb.hp] run return run function rpg:michael_boss_i1/hp_init
# 保险：离场地中心太远或掉到下面就拉回中心；升空的招式除外
execute unless entity @s[tag=rpg.mkb.air] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] unless entity @s[distance=..36] run function rpg:michael_boss_i1/safety/back
execute unless entity @s[tag=rpg.mkb.air] at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] positioned ~-48 ~-80 ~-48 if entity @s[dx=96,dy=72,dz=96] run function rpg:michael_boss_i1/safety/back
scoreboard players operation #m rpg_mk_i1 = #tick rpg_mk_i1
scoreboard players set #k rpg_mk_i1 4
scoreboard players operation #m rpg_mk_i1 %= #k rpg_mk_i1
execute if score #m rpg_mk_i1 matches 0 run function rpg:michael_boss_i1/read_hp
execute if score #m rpg_mk_i1 matches 0 if score #pro rpg_mk_i1 matches 1 run function #rpg:michael_boss_i1/prologue_hp
execute if score @s rpg_mk_i1 matches 1 if score @s rpg_mk_h matches ..1 unless score #pro rpg_mk_i1 matches 1 run return run function rpg:michael_boss_i1/stage/end1
execute if score @s rpg_mk_i1 matches 2 if score @s rpg_mk_h matches ..1 run return run function rpg:michael_boss_i1/stage/end2
execute if entity @s[tag=rpg.mkb.morph] run return run function rpg:michael_boss_i1/morph/tick
execute if score @s rpg_mk_so matches 1.. run function rpg:michael_boss_i1/solid/tick
execute unless entity @s[tag=rpg.mkb.solid] run function rpg:michael_boss_i1/aura
scoreboard players add @s rpg_mk_c 1
execute if score @s rpg_mk_sk matches 1.. run function rpg:michael_boss_i1/sk/tick
execute if score @s rpg_mk_busy matches 1.. run return run scoreboard players remove @s rpg_mk_busy 1
function rpg:michael_boss_i1/schedule
