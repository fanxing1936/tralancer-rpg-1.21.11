# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run rotate @s ~ 0
function rpg:lucifer_p2/anim/tick
execute if entity @s[tag=rpg.hurt] if entity @s[nbt={HurtTime:10s}] run function rpg:lucifer_p2/hurt
execute if predicate rpg:lucifer_p2/glowing unless entity @s[tag=rpg.lu2.glow] run function rpg:lucifer_p2/glow_on
execute unless predicate rpg:lucifer_p2/glowing if entity @s[tag=rpg.lu2.glow] run function rpg:lucifer_p2/glow_off
execute if entity @s[tag=rpg.lu2.flower] run function rpg:lucifer_p2/flower/tick
