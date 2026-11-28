kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
scoreboard players set #cut rpg_pr_i4 0
gamemode adventure @a[tag=rpg.pri4]
execute as @a[tag=rpg.pri4] in rpg:armageddon_4 run tp @s -6 81 0 -90 0
function rpg:prologue_i4/michael/start
