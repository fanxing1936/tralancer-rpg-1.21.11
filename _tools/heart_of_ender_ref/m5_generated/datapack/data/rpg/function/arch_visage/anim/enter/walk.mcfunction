execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
function rpg:arch_visage/internal/stop_sounds
scoreboard players set @s rpg_av_anim 1
scoreboard players set @s rpg_av_t 0
scoreboard players set @s rpg_av_run 1
function rpg:arch_visage/anim/walk/f0
execute on passengers if entity @s[tag=rpg.av.part] run data merge entity @s {interpolation_duration:0}
