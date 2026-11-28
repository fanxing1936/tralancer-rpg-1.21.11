function rpg:prologue_i4/sub/d03
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] run function rpg:prologue_beelzebub/anim/enter/fold
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_4 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] -0.6 82.7 0.6 115.0 0.0
