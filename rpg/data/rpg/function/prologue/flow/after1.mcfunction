kill @e[type=minecraft:item_display,tag=rpg.pr.cam]
scoreboard players set #cut rpg_pr 0
gamemode adventure @a[tag=rpg.pr]
execute as @a[tag=rpg.pr] run function rpg:prologue/player/to_west
function rpg:prologue/music/waves
scoreboard players set #state rpg_pr 4
scoreboard players set #wave rpg_pr 0
scoreboard players set #wt rpg_pr 0
