# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:pope/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:pope/hurt
execute if predicate rpg:pope/ambient run playsound rpg:pope.idle hostile @a[distance=..16] ~ ~ ~ 1 1
