scoreboard players add #wave rpg_pr_i2 10
scoreboard players set #wt rpg_pr_i2 0
function rpg:prologue_i2/sub/t08
execute as @a[tag=rpg.pri2] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2
