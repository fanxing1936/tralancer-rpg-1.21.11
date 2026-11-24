summon minecraft:husk ~ ~1 ~ {Tags:["rpg.pl.g","rpg.pl.s","rpg.pl.gn"],PersistenceRequired:1b}
scoreboard players set #sef rpg_el 8
execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/make
execute as @e[tag=rpg.pl.gn,tag=!rpg.el.boss] at @s run function rpg:elite/champion
execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/stats
execute as @e[tag=rpg.pl.gn] at @s run function rpg:elite/name_pick
tag @e[tag=rpg.pl.gn] remove rpg.pl.gn
