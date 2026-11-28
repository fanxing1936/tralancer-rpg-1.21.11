execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] run function rpg:prologue_i1/cut/kill_actor
particle minecraft:end_rod 0 99.6 -2 0.8 1.5 0.8 0.15 160
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 1 1.4
