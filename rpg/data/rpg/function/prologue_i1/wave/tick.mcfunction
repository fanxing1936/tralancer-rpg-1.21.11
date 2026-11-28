scoreboard players add #wt rpg_pr_i1 1
execute if score #wave rpg_pr_i1 matches 0 if score #wt rpg_pr_i1 matches 20 run function rpg:prologue_i1/wave/start1
execute if score #wave rpg_pr_i1 matches 3 run function rpg:prologue_i1/throne/tick
execute store result score #foe rpg_pr_i1 if entity @e[tag=rpg.pr.foe,distance=0..]
execute if score #wave rpg_pr_i1 matches 1..3 if score #wt rpg_pr_i1 matches 60.. if score #foe rpg_pr_i1 matches 0 run function rpg:prologue_i1/wave/cleared
execute if score #wave rpg_pr_i1 matches 11 if score #wt rpg_pr_i1 matches 80 run function rpg:prologue_i1/wave/start2
execute if score #wave rpg_pr_i1 matches 12 if score #wt rpg_pr_i1 matches 80 run function rpg:prologue_i1/wave/start3
execute if score #wave rpg_pr_i1 matches 13 if score #wt rpg_pr_i1 matches 40 run function rpg:prologue_i1/sub/t09
execute if score #wave rpg_pr_i1 matches 13 in rpg:armageddon positioned 0 81 0 if entity @a[tag=rpg.pri1,gamemode=adventure,distance=..6] run function rpg:prologue_i1/flow/cut3
execute as @e[tag=rpg.pr.foe,distance=0..] at @s in rpg:armageddon positioned 0 81 0 unless entity @s[distance=..75] run function rpg:prologue_i1/cut/kill_actor
