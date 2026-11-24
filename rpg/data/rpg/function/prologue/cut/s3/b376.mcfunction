execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] run function rpg:prologue_lucifer/anim/enter/idle
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 2.5 83.0 3.0 108.6 7.8
