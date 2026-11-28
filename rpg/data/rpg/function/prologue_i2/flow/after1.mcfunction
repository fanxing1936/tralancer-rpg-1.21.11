kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
scoreboard players set #cut rpg_pr_i2 0
gamemode adventure @a[tag=rpg.pri2]
execute as @a[tag=rpg.pri2] run function rpg:prologue_i2/player/to_west
function rpg:prologue_i2/music/waves
scoreboard players set #state rpg_pr_i2 4
scoreboard players set #wave rpg_pr_i2 0
scoreboard players set #wt rpg_pr_i2 0
