execute unless entity @s[type=minecraft:armor_stand,tag=rpg.he] run return 0
function rpg:heart_of_ender/internal/stop_sounds
execute on passengers if entity @s[tag=rpg.he.part] run kill @s
kill @s
