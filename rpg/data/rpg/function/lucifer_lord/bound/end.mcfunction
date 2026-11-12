tag @s remove rpg.lu.bound
execute on passengers if entity @s[tag=rpg.lu.part] run data merge entity @s {Glowing:0b}
function rpg:lucifer_lord/anim/enter/idle
