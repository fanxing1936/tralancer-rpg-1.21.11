tag @s add rpg.lu2.glow
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.lu2.part] run data merge entity @s {Glowing:1b}
