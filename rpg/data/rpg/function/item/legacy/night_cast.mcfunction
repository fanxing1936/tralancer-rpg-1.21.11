# 漆黑之日 · 漆黑之刃：一次可读的环斩，不再对每个实体各召一枚 TNT。
scoreboard players set @s rpg_night_chg 31
tag @a[tag=rpg.night.source] remove rpg.night.source
tag @s add rpg.night.source
particle minecraft:flash{color:6684927} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:2.2} ~ ~1 ~ 2.4 0.7 2.4 0.05 90 force
particle minecraft:sweep_attack ~ ~1 ~ 2 0.5 2 0 28 force
execute as @e[distance=0.1..5,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 8 minecraft:magic by @a[tag=rpg.night.source,limit=1]
kill @e[type=#minecraft:arrows,distance=..5]
playsound minecraft:entity.ender_dragon.shoot player @a[distance=..20] ~ ~ ~ 0.8 0.65
tag @s remove rpg.night.source
function rpg:hud/m8
