# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:belial_lord/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:belial_lord/hurt
execute if predicate rpg:belial_lord/ambient run playsound rpg:belial_lord.idle hostile @a[distance=..16] ~ ~ ~ 1 1
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:belial_lord/glowing unless entity @s[tag=rpg.bll.glow] run function rpg:belial_lord/glow_on
execute unless predicate rpg:belial_lord/glowing if entity @s[tag=rpg.bll.glow] run function rpg:belial_lord/glow_off
# 锅里的药水冒发光的气泡
execute if predicate rpg:belial_lord/bubble run particle minecraft:dust{color:[0.85,0.48,0.85],scale:1.1} ~ ~1.45 ~ 0.35 0.05 0.35 0 2 normal
execute if predicate rpg:belial_lord/bubble run particle minecraft:witch ~ ~1.55 ~ 0.3 0.1 0.3 0 1 normal
