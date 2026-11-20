# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:saul/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:saul/hurt
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:saul/glowing unless entity @s[tag=rpg.slm.glow] run function rpg:saul/glow_on
execute unless predicate rpg:saul/glowing if entity @s[tag=rpg.slm.glow] run function rpg:saul/glow_off
