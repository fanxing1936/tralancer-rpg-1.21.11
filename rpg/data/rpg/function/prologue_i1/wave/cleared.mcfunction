scoreboard players add #wave rpg_pr_i1 10
scoreboard players set #wt rpg_pr_i1 0
function rpg:prologue_i1/sub/t08
execute as @a[tag=rpg.pri1] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2
