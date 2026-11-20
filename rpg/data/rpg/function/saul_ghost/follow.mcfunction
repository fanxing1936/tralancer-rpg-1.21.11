# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:saul_ghost/anim/tick
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:saul_ghost/glowing unless entity @s[tag=rpg.slgm.glow] run function rpg:saul_ghost/glow_on
execute unless predicate rpg:saul_ghost/glowing if entity @s[tag=rpg.slgm.glow] run function rpg:saul_ghost/glow_off
