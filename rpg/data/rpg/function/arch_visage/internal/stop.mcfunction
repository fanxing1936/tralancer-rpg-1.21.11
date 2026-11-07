execute unless entity @s[type=minecraft:armor_stand,tag=rpg.av] run return 0
scoreboard players set @s rpg_av_anim 0
scoreboard players set @s rpg_av_t 0
function rpg:arch_visage/anim/idle/f0
function rpg:arch_visage/internal/pause
