execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub] run function rpg:prologue_beelzebub/anim/enter/talk
function rpg:prologue/sub/d02
particle minecraft:spore_blossom_air -5.6 82.5 -5.2 0.6 0.6 0.6 0 6
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] -6.069 82.75 -2.035 -171.6 3.6
