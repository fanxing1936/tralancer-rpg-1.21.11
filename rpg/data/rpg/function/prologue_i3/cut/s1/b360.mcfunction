function rpg:prologue_i3/sub/n03
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_3 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 44.0 92.0 6.0 98.0 -12.0
execute in rpg:armageddon_3 positioned 0 81 0 run particle minecraft:end_rod ~ ~60 ~ 0.3 30 0.3 0.02 120 force
