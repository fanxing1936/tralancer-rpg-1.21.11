function rpg:prologue/sub/n05
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -20.0 100.0 -30.0 -30.0 30.0
