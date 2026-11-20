# 部件骑在载体上：位置随载体，朝向每刻对齐载体身体朝向；姿势交给动画。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.mis.part] run rotate @s ~ 0
function rpg:michael_spirit/anim/tick
