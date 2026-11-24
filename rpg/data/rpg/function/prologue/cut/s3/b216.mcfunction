execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.belial] run function rpg:prologue_belial/anim/enter/talk
function rpg:prologue/sub/d04
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -6.519 82.75 -0.925 46.9 3.4
