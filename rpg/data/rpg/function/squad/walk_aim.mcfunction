# 按编号错开地压上去。没编号的走 0 号。
execute if entity @s[scores={rpg_sq_slot=0}] run return run function rpg:squad/walk_aim0
execute if entity @s[scores={rpg_sq_slot=1}] run return run function rpg:squad/walk_aim1
execute if entity @s[scores={rpg_sq_slot=2}] run return run function rpg:squad/walk_aim2
execute if entity @s[scores={rpg_sq_slot=3}] run return run function rpg:squad/walk_aim3
function rpg:squad/walk_aim0
