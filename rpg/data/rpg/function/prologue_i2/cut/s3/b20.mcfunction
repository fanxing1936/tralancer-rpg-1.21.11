execute in rpg:armageddon_2 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] -8.30968 81 -6.69032 -61.2 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.belial,distance=0..] -12.1515 81 2.50303 -109.3 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.mammon,distance=0..] -8.14375 81 7.625 -119.7 0
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/anim/enter/address
function rpg:prologue_i2/sub/d01
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 0.5 82.6 2.6 125.0 5.0
