scoreboard players set @s rpg_blil_cd 30
tag @a[tag=rpg.blil.source] remove rpg.blil.source
tag @s add rpg.blil.source
particle minecraft:flash{color:6684825} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.4,0.0,0.6],to_color:[0.0,0.0,0.0],scale:2.2} ~ ~1 ~ 3.5 0.8 3.5 0.06 100 force
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:slowness 3 10 true
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run effect give @s minecraft:weakness 3 3 true
execute as @e[distance=0.1..7,type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb] run damage @s 4 minecraft:magic by @a[tag=rpg.blil.source,limit=1]
playsound minecraft:entity.evoker.prepare_summon player @a[distance=..24] ~ ~ ~ 0.9 0.55
tag @s remove rpg.blil.source
function rpg:hud/m5
