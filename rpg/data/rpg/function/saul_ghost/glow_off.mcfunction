tag @s remove rpg.slgm.glow
execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:0b}
