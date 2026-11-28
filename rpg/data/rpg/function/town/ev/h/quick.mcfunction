tag @e[tag=rpg.te.hol] remove rpg.te.seen
execute as @a[tag=rpg.tw.in] at @s anchored eyes run function rpg:town/ev/h/look
execute as @e[tag=rpg.te.hol,tag=rpg.te.seen,tag=!rpg.te.big] run data modify entity @s NoAI set value 1b
execute as @e[tag=rpg.te.hol,tag=!rpg.te.seen] run data modify entity @s NoAI set value 0b
