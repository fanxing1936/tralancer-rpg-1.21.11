execute at @s run particle minecraft:crit ~ ~1 ~ 0.2 0.4 0.2 0.2 12
execute at @s run playsound minecraft:block.note_block.bell player @a[distance=..12] ~ ~ ~ 1 1.6
execute at @s run scoreboard players add @p[tag=rpg.tl.bet] rpg_tl_hit 1
execute at @s run function rpg:town/life/q/target_die
