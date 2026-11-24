scoreboard players set #c2 rpg_pl 0
scoreboard players set #f2 rpg_pl 0
setblock ~ ~1 ~ minecraft:air
kill @e[type=#rpg:elite_pool,distance=..26]
execute as @e[tag=rpg.pl.g,distance=..30] run tp @s ~ -200 ~
stopsound @a[distance=..64] record rpg:bgm.prologue_waves
