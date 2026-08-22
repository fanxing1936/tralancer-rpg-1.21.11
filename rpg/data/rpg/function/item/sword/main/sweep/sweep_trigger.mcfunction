execute as @a[scores={sweep=50..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"sweep_atk"}],Invulnerable:1b}
execute as @a[scores={sweep=50..}] anchored eyes at @s run playsound minecraft:entity.player.attack.crit player @s
execute as @e[name=sweep_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={sweep=50..}]
execute as @a[scores={sweep=50..}] anchored eyes at @s run scoreboard players set @s sweep 0
execute as @e[name=sweep_atk,type=armor_stand] anchored eyes at @s run particle sweep_attack ~0.25 ~0.5 ~0.25 -0.5 -0.5 -0.5 1 20

execute as @e[name=sweep_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=sweep_atk,type=armor_stand] anchored feet at @s run effect give @e[distance=0.1..1.5] wither 5 10 true