scoreboard players add #tt rpg_te 1
execute as @a[tag=rpg.tw.in,scores={rpg_te_v=1..}] run function rpg:town/ev/g/judged
execute if score #tt rpg_te matches 160.. run function rpg:town/ev/g/judge_default
