summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew","rpg.mkb.spoke"]}
execute as @e[tag=rpg.mkb.fxnew,distance=0..] run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 60
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
