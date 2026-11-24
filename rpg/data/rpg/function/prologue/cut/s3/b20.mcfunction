execute in rpg:armageddon run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub] -8.30968 81 -6.69032 -61.2 0
execute in rpg:armageddon run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.belial] -12.1515 81 2.50303 -109.3 0
execute in rpg:armageddon run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.mammon] -8.14375 81 7.625 -119.7 0
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] run function rpg:prologue_lucifer/anim/enter/address
function rpg:prologue/sub/d01
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 0.5 82.6 2.6 125.0 5.0
