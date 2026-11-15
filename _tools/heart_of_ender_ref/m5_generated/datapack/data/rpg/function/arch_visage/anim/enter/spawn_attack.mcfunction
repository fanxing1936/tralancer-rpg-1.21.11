execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
function rpg:arch_visage/internal/stop_sounds
scoreboard players set @s rpg_av_anim 2
scoreboard players set @s rpg_av_t 0
scoreboard players set @s rpg_av_run 1
playsound rpg:arch_visage.tele_in hostile @a[distance=..24] ~ ~ ~ 1 1
function rpg:arch_visage/anim/spawn_attack/f0
execute on passengers if entity @s[tag=rpg.av.part] run data merge entity @s {interpolation_duration:0}
