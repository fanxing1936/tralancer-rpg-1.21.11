function rpg:prologue_i3/music/michael
execute in rpg:armageddon_3 run particle minecraft:end_rod 4 101 0 0.2 20 0.2 0.02 200 force
execute as @a[tag=rpg.pri3] at @s run playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 0.6
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_3 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -3.5 82.8 5.5 -126.3 -54.8
