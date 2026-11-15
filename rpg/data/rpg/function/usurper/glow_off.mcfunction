tag @s remove rpg.usm.glow
execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:0b}
