function rpg:prologue_i1/sub/d05
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.belial,distance=0..] run function rpg:prologue_belial/anim/enter/idle
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -0.8 82.6 0.4 110.0 0.0
