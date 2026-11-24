stopsound @a[tag=rpg.pr] record
stopsound @a[tag=rpg.pr] music
execute as @a[tag=rpg.pr] at @s run playsound rpg:bgm.prologue_intro record @s ~ ~ ~ 1 1
scoreboard players set #bgm rpg_pr 1537
scoreboard players set #bgmid rpg_pr 1
