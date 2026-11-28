stopsound @a[tag=rpg.pri1] record
stopsound @a[tag=rpg.pri1] music
execute as @a[tag=rpg.pri1] at @s run playsound rpg:bgm.prologue_michael record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_pr_i1 2353
scoreboard players set #bgmid rpg_pr_i1 3
