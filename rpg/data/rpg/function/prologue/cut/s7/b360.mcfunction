function rpg:prologue/sub/n08
scoreboard players set #aura rpg_pr 0
particle minecraft:large_smoke 0 39 0 2 3 2 0.02 120
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value 0
execute in rpg:armageddon run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] 0.3 92.0 0.3 -90.0 90.0
