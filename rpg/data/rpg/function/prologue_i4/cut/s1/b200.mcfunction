function rpg:prologue_i4/sub/n02
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_4 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 30.0 84.0 -16.0 0.0 8.0
