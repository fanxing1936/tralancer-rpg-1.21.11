scoreboard players set #smoke rpg_pr_i2 1
function rpg:prologue_i2/sub/n06
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_2 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 0.3 95.6 0.3 -90.0 90.0
