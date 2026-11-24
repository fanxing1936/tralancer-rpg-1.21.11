function rpg:prologue/sub/n02
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 30.0 84.0 -16.0 0.0 8.0
