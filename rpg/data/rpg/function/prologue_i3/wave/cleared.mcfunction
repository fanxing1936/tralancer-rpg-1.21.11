scoreboard players add #wave rpg_pr_i3 10
scoreboard players set #wt rpg_pr_i3 0
function rpg:prologue_i3/sub/t08
execute as @a[tag=rpg.pri3] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6 1.2
