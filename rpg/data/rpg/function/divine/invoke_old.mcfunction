scoreboard players set @s rpg_lt_div_cd 600
scoreboard players set @s rpg_lt_div_max 600
tag @s add rpg.divine.cast
execute as @e[tag=rpg.demon,distance=..10] at @s run function rpg:divine/damage/old_target
execute as @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..10] at @s run function rpg:divine/damage/old_target
execute as @e[tag=rpg.demon.fly,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..10] at @s run function rpg:divine/damage/old_target
tag @s remove rpg.divine.cast
particle minecraft:flash{color:16771482} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:totem_of_undying ~ ~1 ~ 5 1 5 0.08 130 force
particle minecraft:end_rod ~ ~0.8 ~ 4.8 0.5 4.8 0.03 90 force
playsound minecraft:block.beacon.power_select master @a[distance=..24] ~ ~ ~ 1 1.35
function rpg:hud/m59
