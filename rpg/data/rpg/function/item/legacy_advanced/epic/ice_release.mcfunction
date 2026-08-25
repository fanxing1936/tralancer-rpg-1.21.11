
scoreboard players set @s ice_step 0
playsound minecraft:entity.player.hurt_freeze player @s ~ ~ ~ 1 0.8
particle dust_pillar{block_state:{Name:blue_ice}} ~ ~1 ~ 2.5 1 2.5 0.15 50 force
effect give @e[distance=0.1..5,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand] slowness 4 4 true
tag @e[tag=rpg.ice.cast] remove rpg.ice.cast
tag @s add rpg.ice.cast
execute as @e[distance=0.1..5,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker,type=!minecraft:armor_stand] run damage @s 6 minecraft:freeze by @a[tag=rpg.ice.cast,limit=1]
tag @s remove rpg.ice.cast
function rpg:hud/m14
