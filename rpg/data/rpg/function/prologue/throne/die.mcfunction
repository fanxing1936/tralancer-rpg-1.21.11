execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run particle minecraft:end_rod ~ ~ ~ 1.5 1.5 1.5 0.2 120
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] at @s run playsound minecraft:entity.generic.explode master @a[tag=rpg.pr] ~ ~ ~ 1.5 0.8
execute as @e[type=minecraft:vindicator,tag=rpg.pr.throne] run function rpg:prologue/cut/kill_actor
