function rpg:prologue/sub/n03
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 44.0 92.0 6.0 98.0 -12.0
execute in rpg:armageddon positioned 0 81 0 run particle minecraft:end_rod ~ ~60 ~ 0.3 30 0.3 0.02 120 force
