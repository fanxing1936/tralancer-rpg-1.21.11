execute unless entity @s[type=minecraft:armor_stand,tag=rpg.he] run return 0
scoreboard players set @s rpg_he_run 0
execute on passengers if entity @s[tag=rpg.he.part] run data merge entity @s {start_interpolation:0,interpolation_duration:0}
function rpg:heart_of_ender/internal/stop_sounds
