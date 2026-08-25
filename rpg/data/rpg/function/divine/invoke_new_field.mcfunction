scoreboard players set @s rpg_lt_div_cd 600
scoreboard players set @s rpg_lt_div_max 600
tag @s add rpg.divine.cast
execute as @e[tag=rpg.demon,distance=..8] at @s run function rpg:divine/damage/field_target
execute as @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] at @s run function rpg:divine/damage/field_target
execute as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] at @s run function rpg:divine/damage/field_target
tag @s remove rpg.divine.cast
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:blindness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:darkness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:wither
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:poison
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:slowness
execute as @a[distance=..8,gamemode=!spectator] run effect clear @s minecraft:weakness
effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 6 1 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:resistance 6 0 true
effect give @a[distance=..8,gamemode=!spectator] minecraft:absorption 6 1 true
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~3.000 ~0.08 ~0.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.898 ~0.08 ~0.776 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.598 ~0.08 ~1.500 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.121 ~0.08 ~2.121 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~1.500 ~0.08 ~2.598 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~0.776 ~0.08 ~2.898 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~0.000 ~0.08 ~3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-0.776 ~0.08 ~2.898 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-1.500 ~0.08 ~2.598 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.121 ~0.08 ~2.121 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.598 ~0.08 ~1.500 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.898 ~0.08 ~0.776 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-3.000 ~0.08 ~0.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.898 ~0.08 ~-0.776 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.598 ~0.08 ~-1.500 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-2.121 ~0.08 ~-2.121 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-1.500 ~0.08 ~-2.598 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-0.776 ~0.08 ~-2.898 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~-0.000 ~0.08 ~-3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~0.776 ~0.08 ~-2.898 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~1.500 ~0.08 ~-2.598 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.121 ~0.08 ~-2.121 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.598 ~0.08 ~-1.500 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.00} ~2.898 ~0.08 ~-0.776 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~6.000 ~0.08 ~0.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.909 ~0.08 ~1.042 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.638 ~0.08 ~2.052 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.196 ~0.08 ~3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~4.596 ~0.08 ~3.857 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~3.857 ~0.08 ~4.596 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~3.000 ~0.08 ~5.196 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~2.052 ~0.08 ~5.638 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~1.042 ~0.08 ~5.909 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~0.000 ~0.08 ~6.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-1.042 ~0.08 ~5.909 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-2.052 ~0.08 ~5.638 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-3.000 ~0.08 ~5.196 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-3.857 ~0.08 ~4.596 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-4.596 ~0.08 ~3.857 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.196 ~0.08 ~3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.638 ~0.08 ~2.052 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.909 ~0.08 ~1.042 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-6.000 ~0.08 ~0.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.909 ~0.08 ~-1.042 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.638 ~0.08 ~-2.052 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-5.196 ~0.08 ~-3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-4.596 ~0.08 ~-3.857 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-3.857 ~0.08 ~-4.596 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-3.000 ~0.08 ~-5.196 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-2.052 ~0.08 ~-5.638 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-1.042 ~0.08 ~-5.909 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~-0.000 ~0.08 ~-6.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~1.042 ~0.08 ~-5.909 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~2.052 ~0.08 ~-5.638 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~3.000 ~0.08 ~-5.196 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~3.857 ~0.08 ~-4.596 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~4.596 ~0.08 ~-3.857 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.196 ~0.08 ~-3.000 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.638 ~0.08 ~-2.052 0 0 0 0 1 force
particle dust{color:[0.38,0.85,0.91],scale:1.25} ~5.909 ~0.08 ~-1.042 0 0 0 0 1 force
particle minecraft:flash{color:6482395} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~0.8 ~ 5.5 0.5 5.5 0.05 120 force
playsound minecraft:block.beacon.power_select master @a[distance=..32] ~ ~ ~ 1 0.85
playsound minecraft:block.amethyst_block.resonate master @a[distance=..24] ~ ~ ~ 0.8 1.55
function rpg:hud/m61
