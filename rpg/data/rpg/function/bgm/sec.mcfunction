scoreboard players set #t rpg_bgm 0
execute store result score #day rpg_bgm run time query daytime
execute as @a at @s run function rpg:bgm/player
