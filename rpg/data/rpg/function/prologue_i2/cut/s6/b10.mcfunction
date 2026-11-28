execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer,distance=0..] run function rpg:prologue_lucifer/anim/enter/seized
scoreboard players set #aura rpg_pr_i2 1
particle minecraft:sculk_soul 0 91 0 0.8 1 0.8 0.02 30
