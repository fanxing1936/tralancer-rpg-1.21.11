function rpg:prologue/sub/n04
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -37.0 84.2 0.0 -90.0 5.0
