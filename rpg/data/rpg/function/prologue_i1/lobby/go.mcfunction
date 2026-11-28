execute as @a[tag=rpg.pri1] run function rpg:prologue_i1/role/kit
kill @e[type=minecraft:marker,tag=rpg.pr.altar,distance=0..]
kill @e[type=minecraft:text_display,tag=rpg.pr.deco,distance=0..]
function rpg:prologue_i1/sub/clear
function rpg:prologue_i1/flow/cut1
