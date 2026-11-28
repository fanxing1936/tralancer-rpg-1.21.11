execute as @a[scores={rpg_tl_dc=1..}] at @s run function rpg:town/life/died
execute as @a[scores={rpg_tl_do=1..}] at @s run function rpg:town/life/do
execute as @e[type=minecraft:interaction,tag=rpg.tl.target] if data entity @s attack run function rpg:town/life/q/target_hit
