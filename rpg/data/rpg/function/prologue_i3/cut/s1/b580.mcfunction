function rpg:prologue_i3/sub/n05
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_3 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -20.0 100.0 -30.0 -30.0 30.0
