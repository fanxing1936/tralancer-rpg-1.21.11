tag @s add rpg.dm.cast
tag @e[tag=rpg.unit] remove rpg.lu2f.saw
execute as @e[tag=rpg.unit.f,distance=..22] at @s anchored eyes run function rpg:lucifer_fight/gaze/look
execute as @e[tag=rpg.unit,tag=rpg.lu2f.saw] positioned ~ ~8.4 ~ facing entity @s eyes run function rpg:lucifer_fight/fx/gline
execute as @e[tag=rpg.unit,tag=rpg.lu2f.saw] run function rpg:lucifer_fight/gaze/hit
tag @e[tag=rpg.unit] remove rpg.lu2f.saw
tag @s remove rpg.dm.cast
particle flash{color:6280844} ~ ~4.5 ~ 0 0 0 0 1
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~4.5 ~ 1 0.5 1 0.1 40
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 0.8 0.7
