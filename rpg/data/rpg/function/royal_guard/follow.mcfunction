# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:royal_guard/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:royal_guard/hurt
execute if predicate rpg:royal_guard/ambient run playsound rpg:royal_guard.idle hostile @a[distance=..16] ~ ~ ~ 0.5 1
function rpg:royal_guard/ai/tick
