execute as @a[scores={flame=50..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"flame_atk"}],Invulnerable:1b}
execute as @a[scores={flame=50..}] anchored eyes at @s run playsound minecraft:entity.blaze.shoot player @s
execute as @e[name=flame_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={flame=50..}]
execute as @a[scores={flame=50..}] anchored eyes at @s run scoreboard players set @s flame 0
execute as @e[name=flame_atk,type=armor_stand] anchored eyes at @s run particle flame ~0.25 ~0.5 ~0.25 -0.5 -0.5 -0.5 0.1 20
execute as @e[name=flame_atk,type=armor_stand] anchored eyes at @s run particle large_smoke ~0.25 ~0.5 ~0.25 -0.5 -0.5 -0.5 0.1 20

execute as @e[name=flame_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=flame_atk,type=armor_stand] anchored feet at @s as @e[distance=0.1..1.5] run damage @s 17 minecraft:in_fire