data modify storage rpg:lucifer_lord held set value {}
execute if entity @s[tag=rpg.lu.original_hand] on passengers if entity @s[tag=rpg.lu.p.weapon] run data modify storage rpg:lucifer_lord held set from entity @s item
execute if entity @s[tag=rpg.lu.original_hand] run data modify entity @s equipment.mainhand set from storage rpg:lucifer_lord held
execute on passengers if entity @s[tag=rpg.lu.part] run kill @s
tag @s remove rpg.lu
tag @s remove rpg.lu.bound
tag @s remove rpg.lu.glow
tag @s remove rpg.lu.original_hand
