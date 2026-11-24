scoreboard players add #t rpg_sef 1
execute as @a[scores={rpg_sef_do=1..}] at @s run function rpg:sephira/press
scoreboard players operation #m rpg_sef = #t rpg_sef
scoreboard players operation #m rpg_sef %= #20 rpg_sef
execute unless score #m rpg_sef matches 0 run return 0
scoreboard players operation #m2 rpg_sef = #t rpg_sef
scoreboard players operation #m2 rpg_sef %= #40 rpg_sef
execute store result score #day rpg_sef run time query day
execute as @a[tag=!rpg.ob.hold,tag=!rpg.pr] at @s run function rpg:sephira/sec
