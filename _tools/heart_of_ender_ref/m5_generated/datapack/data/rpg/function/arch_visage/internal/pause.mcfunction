execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
scoreboard players set @s rpg_av_run 0
execute on passengers if entity @s[tag=rpg.av.part] run data merge entity @s {start_interpolation:0,interpolation_duration:0}
function rpg:arch_visage/internal/stop_sounds
