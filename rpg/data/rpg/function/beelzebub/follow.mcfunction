# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:beelzebub/anim/tick
execute if entity @s[nbt={HurtTime:10s}] run function rpg:beelzebub/hurt
execute if predicate rpg:beelzebub/ambient run playsound rpg:beelzebub.idle hostile @a[distance=..16] ~ ~ ~ 1 1
execute if predicate rpg:beelzebub/distant run playsound rpg:beelzebub.distant hostile @a[distance=20..64] ~ ~ ~ 0.8 1
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:beelzebub/glowing unless entity @s[tag=rpg.bz.glow] run function rpg:beelzebub/glow_on
execute unless predicate rpg:beelzebub/glowing if entity @s[tag=rpg.bz.glow] run function rpg:beelzebub/glow_off
