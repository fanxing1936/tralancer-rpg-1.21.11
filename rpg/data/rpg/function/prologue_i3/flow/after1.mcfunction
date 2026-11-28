kill @e[type=minecraft:item_display,tag=rpg.pr.cam,distance=0..]
scoreboard players set #cut rpg_pr_i3 0
gamemode adventure @a[tag=rpg.pri3]
execute as @a[tag=rpg.pri3] run function rpg:prologue_i3/player/to_west
function rpg:prologue_i3/music/waves
scoreboard players set #state rpg_pr_i3 4
scoreboard players set #wave rpg_pr_i3 0
scoreboard players set #wt rpg_pr_i3 0
