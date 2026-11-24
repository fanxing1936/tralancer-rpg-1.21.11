execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] run function rpg:prologue_lucifer/anim/enter/reach
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 3.0 82.2 3.0 161.6 -2.4
