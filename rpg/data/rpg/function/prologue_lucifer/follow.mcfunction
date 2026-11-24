# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers run rotate @s ~ 0
function rpg:prologue_lucifer/anim/tick
# 被法阵束缚时载体发光：部件一起发光
execute if predicate rpg:prologue_lucifer/glowing unless entity @s[tag=rpg.prlu.glow] run function rpg:prologue_lucifer/glow_on
execute unless predicate rpg:prologue_lucifer/glowing if entity @s[tag=rpg.prlu.glow] run function rpg:prologue_lucifer/glow_off
