# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:mammon_lord/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:mammon_lord/hurt
execute if predicate rpg:mammon_lord/ambient run playsound rpg:mammon_lord.idle hostile @a[distance=..16] ~ ~ ~ 1 1
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:mammon_lord/glowing unless entity @s[tag=rpg.mml.glow] run function rpg:mammon_lord/glow_on
execute unless predicate rpg:mammon_lord/glowing if entity @s[tag=rpg.mml.glow] run function rpg:mammon_lord/glow_off
