# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:leviathan/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:leviathan/hurt
execute if predicate rpg:leviathan/ambient run playsound rpg:leviathan.idle hostile @a[distance=..16] ~ ~ ~ 1 1
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:leviathan/glowing unless entity @s[tag=rpg.lv.glow] run function rpg:leviathan/glow_on
execute unless predicate rpg:leviathan/glowing if entity @s[tag=rpg.lv.glow] run function rpg:leviathan/glow_off
