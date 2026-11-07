execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
function rpg:arch_visage/internal/stop_sounds
execute on passengers if entity @s[tag=rpg.av.part] run kill @s
kill @s
