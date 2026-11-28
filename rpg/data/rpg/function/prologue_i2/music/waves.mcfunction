stopsound @a[tag=rpg.pri2] record
stopsound @a[tag=rpg.pri2] music
execute as @a[tag=rpg.pri2] at @s run playsound rpg:bgm.prologue_waves record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_pr_i2 1667
scoreboard players set #bgmid rpg_pr_i2 2
