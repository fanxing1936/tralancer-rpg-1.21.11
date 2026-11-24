execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.mammon] run function rpg:prologue_mammon/anim/enter/talk
function rpg:prologue/sub/d06
particle minecraft:wax_on -4.6 82.6 5.6 0.4 0.4 0.4 0 8
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -5.645 82.75 2.575 -19.1 3.6
