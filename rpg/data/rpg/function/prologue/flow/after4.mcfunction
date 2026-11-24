kill @e[type=minecraft:item_display,tag=rpg.pr.cam]
scoreboard players set #cut rpg_pr 0
gamemode adventure @a[tag=rpg.pr]
execute as @a[tag=rpg.pr] in rpg:armageddon run tp @s -6 81 0 -90 0
function rpg:prologue/michael/start
