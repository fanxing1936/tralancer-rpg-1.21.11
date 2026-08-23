# 点金：贪婪不制造东西，它只让已有的东西变多。
particle happy_villager ~ ~1 ~ 3 1 3 0.2 80
particle wax_on ~ ~1 ~ 3 1 3 0.1 60
particle end_rod ~ ~1 ~ 2.5 1 2.5 0.05 40
playsound minecraft:block.amethyst_block.chime player @a[distance=..24] ~ ~ ~ 1 1.4
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.8 1.6
execute as @e[type=minecraft:item,distance=..8] at @s run function rpg:pact/p7_gild
summon minecraft:experience_orb ~ ~1 ~ {Value:60}
