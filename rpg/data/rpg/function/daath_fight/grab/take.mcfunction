execute positioned ^ ^ ^1.2 run tag @a[distance=..2.0,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute as @a[tag=rpg.dt.hit] at @s run tp @s ~ ~0.3 ~
execute as @a[tag=rpg.dt.hit] run effect give @s minecraft:levitation 1 6 true
execute if entity @a[tag=rpg.dt.hit] run playsound minecraft:entity.player.attack.knockback hostile @a[distance=..48] ~ ~ ~ 1.2 0.6
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 14
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
particle minecraft:cloud ~0.40 ~0.20 ~0.00 1.000 0.000 0.000 0.2 0 force
particle minecraft:cloud ~0.35 ~0.20 ~0.20 0.866 0.000 0.500 0.2 0 force
particle minecraft:cloud ~0.20 ~0.20 ~0.35 0.500 0.000 0.866 0.2 0 force
particle minecraft:cloud ~0.00 ~0.20 ~0.40 0.000 0.000 1.000 0.2 0 force
particle minecraft:cloud ~-0.20 ~0.20 ~0.35 -0.500 0.000 0.866 0.2 0 force
particle minecraft:cloud ~-0.35 ~0.20 ~0.20 -0.866 0.000 0.500 0.2 0 force
particle minecraft:cloud ~-0.40 ~0.20 ~0.00 -1.000 0.000 0.000 0.2 0 force
particle minecraft:cloud ~-0.35 ~0.20 ~-0.20 -0.866 0.000 -0.500 0.2 0 force
particle minecraft:cloud ~-0.20 ~0.20 ~-0.35 -0.500 0.000 -0.866 0.2 0 force
particle minecraft:cloud ~-0.00 ~0.20 ~-0.40 -0.000 0.000 -1.000 0.2 0 force
particle minecraft:cloud ~0.20 ~0.20 ~-0.35 0.500 0.000 -0.866 0.2 0 force
particle minecraft:cloud ~0.35 ~0.20 ~-0.20 0.866 0.000 -0.500 0.2 0 force
