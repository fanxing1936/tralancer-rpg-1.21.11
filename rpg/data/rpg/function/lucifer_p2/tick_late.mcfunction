# After command/tick_end: the appearance carrier remains hidden.
execute as @e[type=minecraft:vindicator,scores={rpg_dm_lord=1},tag=rpg.lu2,tag=rpg.lu.phase2] unless predicate rpg:lucifer_p2/invisible run effect give @s minecraft:invisibility infinite 0 true
