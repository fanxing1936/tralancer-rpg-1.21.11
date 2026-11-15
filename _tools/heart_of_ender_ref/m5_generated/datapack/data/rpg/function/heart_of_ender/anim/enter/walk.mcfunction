execute unless entity @s[type=minecraft:armor_stand,tag=rpg.he] run return 0
function rpg:heart_of_ender/internal/stop_sounds
scoreboard players set @s rpg_he_anim 1
scoreboard players set @s rpg_he_t 0
scoreboard players set @s rpg_he_run 1
playsound rpg:heart_of_ender.inner_voice hostile @a[distance=..24] ~ ~ ~ 0.6 1
function rpg:heart_of_ender/anim/walk/f0
execute on passengers if entity @s[tag=rpg.he.part] run data merge entity @s {interpolation_duration:0}
