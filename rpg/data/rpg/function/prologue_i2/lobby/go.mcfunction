execute as @a[tag=rpg.pri2] run function rpg:prologue_i2/role/kit
kill @e[type=minecraft:marker,tag=rpg.pr.altar,distance=0..]
kill @e[type=minecraft:text_display,tag=rpg.pr.deco,distance=0..]
function rpg:prologue_i2/sub/clear
function rpg:prologue_i2/flow/cut1
