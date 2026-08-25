
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2,tag=boss] run effect give @e[limit=1] minecraft:wither 5 3 true
scoreboard players reset * devil_hurt
execute as @e[type=minecraft:vindicator,tag=devil2] at @s run function rpg:entities/warden/phase2_entity
