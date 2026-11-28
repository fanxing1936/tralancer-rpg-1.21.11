scoreboard players add #wt rpg_pr_i4 1
execute if score #wave rpg_pr_i4 matches 0 if score #wt rpg_pr_i4 matches 20 run function rpg:prologue_i4/wave/start1
execute if score #wave rpg_pr_i4 matches 3 run function rpg:prologue_i4/throne/tick
execute store result score #foe rpg_pr_i4 if entity @e[tag=rpg.pr.foe,distance=0..]
execute if score #wave rpg_pr_i4 matches 1..3 if score #wt rpg_pr_i4 matches 60.. if score #foe rpg_pr_i4 matches 0 run function rpg:prologue_i4/wave/cleared
execute if score #wave rpg_pr_i4 matches 11 if score #wt rpg_pr_i4 matches 80 run function rpg:prologue_i4/wave/start2
execute if score #wave rpg_pr_i4 matches 12 if score #wt rpg_pr_i4 matches 80 run function rpg:prologue_i4/wave/start3
execute if score #wave rpg_pr_i4 matches 13 if score #wt rpg_pr_i4 matches 40 run function rpg:prologue_i4/sub/t09
execute if score #wave rpg_pr_i4 matches 13 in rpg:armageddon_4 positioned 0 81 0 if entity @a[tag=rpg.pri4,gamemode=adventure,distance=..6] run function rpg:prologue_i4/flow/cut3
execute as @e[tag=rpg.pr.foe,distance=0..] at @s in rpg:armageddon_4 positioned 0 81 0 unless entity @s[distance=..75] run function rpg:prologue_i4/cut/kill_actor
