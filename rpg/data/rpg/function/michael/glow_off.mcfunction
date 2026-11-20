tag @s remove rpg.mkm.glow
execute on passengers if entity @s[type=minecraft:item_display] run data merge entity @s {Glowing:0b}
