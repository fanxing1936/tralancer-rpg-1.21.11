kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
scoreboard players set #cut rpg_pr_i1 0
gamemode adventure @a[tag=rpg.pri1]
execute as @a[tag=rpg.pri1] in rpg:armageddon run tp @s -6 81 0 -90 0
function rpg:prologue_i1/michael/start
