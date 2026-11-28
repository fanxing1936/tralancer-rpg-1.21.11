execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.mammon,distance=0..] run function rpg:prologue_mammon/anim/enter/kneel_idle
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 3
