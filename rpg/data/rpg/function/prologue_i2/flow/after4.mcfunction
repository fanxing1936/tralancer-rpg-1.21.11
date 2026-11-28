kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
scoreboard players set #cut rpg_pr_i2 0
gamemode adventure @a[tag=rpg.pri2]
execute as @a[tag=rpg.pri2] in rpg:armageddon_2 run tp @s -6 81 0 -90 0
function rpg:prologue_i2/michael/start
