# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:vanguard/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:vanguard/hurt
execute if predicate rpg:vanguard/ambient run playsound rpg:vanguard.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_vg matches 1.. run scoreboard players remove @s rpg_vg 1
execute if score @s rpg_vg matches ..0 unless score @s rpg_vg_anim matches 2..3 if entity @a[distance=..3.2,gamemode=!spectator,gamemode=!creative,limit=1] run function rpg:vanguard/strike
