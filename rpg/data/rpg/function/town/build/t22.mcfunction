# 孤堡（教廷前哨 · 审判官驻地）：positioned 镇中心 y=0；宏参数 sfx、var
$scoreboard players set #var rpg_tw $(var)
$execute positioned ~ $(h) ~ run function rpg:town/pad/t22
data modify storage rpg:town m.sfx set value ""
scoreboard players set #hm rpg_tw -999
execute positioned ~-68 0 ~-59 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~68 0 ~-59 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~-68 0 ~59 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~68 0 ~59 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute positioned ~0 0 ~0 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ #rpg:town_clear run function rpg:town/s/max
execute if score #hm rpg_tw matches -999 run scoreboard players operation #hm rpg_tw = #h0 rpg_tw
scoreboard players remove #hm rpg_tw 1
execute store result storage rpg:town m.y int 1 run scoreboard players get #hm rpg_tw
function rpg:town/t/22/0 with storage rpg:town m
summon minecraft:marker ~ 0 ~ {Tags:["rpg.tw.a","rpg.tw.c","rpg.tw.lm","rpg.tw.new"]}
execute positioned ~0 0 ~65 positioned over motion_blocking_no_leaves run tp @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new] ~ ~ ~
execute positioned ~0 0 ~65 positioned over motion_blocking_no_leaves run function rpg:town/lm/fort
execute as @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new,limit=1] store result score #sx22 rpg_tw run data get entity @s Pos[0]
execute as @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new,limit=1] store result score #sy22 rpg_tw run data get entity @s Pos[1]
execute as @e[type=minecraft:marker,tag=rpg.tw.c,tag=rpg.tw.new,limit=1] store result score #sz22 rpg_tw run data get entity @s Pos[2]
scoreboard players set @e[type=minecraft:marker,tag=rpg.tw.new] rpg_tw_id 22
tag @e[type=minecraft:marker,tag=rpg.tw.new] remove rpg.tw.new
