tag @a[tag=rpg.hunter.source] remove rpg.hunter.source
execute on origin run tag @s add rpg.hunter.source
particle minecraft:flash{color:11534423} ~ ~ ~ 0 0 0 0 1
particle minecraft:squid_ink ~ ~ ~ 1 1 1 0.1 45 force
execute as @e[distance=..3.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows] run effect give @s minecraft:poison 5 1 true
execute as @e[distance=..3.5,type=!minecraft:player,type=!minecraft:item,type=!#minecraft:arrows] run damage @s 7 minecraft:magic by @a[tag=rpg.hunter.source,limit=1]
playsound minecraft:entity.generic.explode player @a[distance=..20] ~ ~ ~ 0.8 1.35
tag @a[tag=rpg.hunter.source] remove rpg.hunter.source
kill @s
