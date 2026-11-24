stopsound @a[tag=rpg.pr] record
stopsound @a[tag=rpg.pr] music
execute as @a[tag=rpg.pr] at @s run playsound rpg:bgm.prologue_michael record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_pr 2353
scoreboard players set #bgmid rpg_pr 3
