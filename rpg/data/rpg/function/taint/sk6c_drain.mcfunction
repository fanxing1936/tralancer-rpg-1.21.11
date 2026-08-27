function rpg:inquest/seal/ability/record_magic
damage @s 6 minecraft:magic by @e[tag=rpg.dm.cast,limit=1]
particle damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 10
effect give @e[tag=rpg.dm.cast,limit=1] minecraft:instant_health 1 1 true
