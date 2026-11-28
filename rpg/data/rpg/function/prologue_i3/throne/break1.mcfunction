tag @s add rpg.pr.thb1
function rpg:prologue_throne/wheel/down
execute at @s run particle minecraft:end_rod ~ ~2 ~ 1 1 1 0.15 40
execute at @s run playsound minecraft:block.glass.break master @a[tag=rpg.pri3] ~ ~ ~ 1.5 0.6
