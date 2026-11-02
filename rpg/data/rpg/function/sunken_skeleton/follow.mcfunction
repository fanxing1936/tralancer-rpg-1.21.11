# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:sunken_skeleton/anim/tick
execute if entity @s[nbt={HurtTime:10s}] run function rpg:sunken_skeleton/hurt
execute if predicate rpg:sunken_skeleton/ambient run playsound rpg:sunken_skeleton.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_sk matches 1.. run scoreboard players remove @s rpg_sk 1
execute if score @s rpg_sk matches ..0 unless score @s rpg_sk_anim matches 2 if entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run function rpg:sunken_skeleton/strike
