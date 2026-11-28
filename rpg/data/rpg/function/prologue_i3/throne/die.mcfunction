execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s run particle minecraft:end_rod ~ ~ ~ 1.5 1.5 1.5 0.2 120
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] at @s run playsound minecraft:entity.generic.explode master @a[tag=rpg.pri3] ~ ~ ~ 1.5 0.8
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne,distance=0..] run function rpg:prologue_i3/cut/kill_actor
