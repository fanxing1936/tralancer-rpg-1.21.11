execute as @a[tag=rpg.pr] run function rpg:prologue/role/kit
kill @e[type=minecraft:marker,tag=rpg.pr.altar]
kill @e[type=minecraft:text_display,tag=rpg.pr.deco]
function rpg:prologue/sub/clear
function rpg:prologue/flow/cut1
