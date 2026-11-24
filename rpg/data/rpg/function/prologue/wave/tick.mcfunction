scoreboard players add #wt rpg_pr 1
execute if score #wave rpg_pr matches 0 if score #wt rpg_pr matches 20 run function rpg:prologue/wave/start1
execute if score #wave rpg_pr matches 3 run function rpg:prologue/throne/tick
execute store result score #foe rpg_pr if entity @e[tag=rpg.pr.foe]
execute if score #wave rpg_pr matches 1..3 if score #wt rpg_pr matches 60.. if score #foe rpg_pr matches 0 run function rpg:prologue/wave/cleared
execute if score #wave rpg_pr matches 11 if score #wt rpg_pr matches 80 run function rpg:prologue/wave/start2
execute if score #wave rpg_pr matches 12 if score #wt rpg_pr matches 80 run function rpg:prologue/wave/start3
execute if score #wave rpg_pr matches 13 if score #wt rpg_pr matches 40 run function rpg:prologue/sub/t09
execute if score #wave rpg_pr matches 13 in rpg:armageddon positioned 0 81 0 if entity @a[tag=rpg.pr,gamemode=adventure,distance=..6] run function rpg:prologue/flow/cut3
execute as @e[tag=rpg.pr.foe] at @s in rpg:armageddon positioned 0 81 0 unless entity @s[distance=..75] run function rpg:prologue/cut/kill_actor
