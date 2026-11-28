# prologue_multi hub
# 每秒：排队的人分进空闲的战场（四人一组）
scoreboard players set #sec rpg_prh 0
execute store result score #q rpg_prh if entity @a[tag=rpg.pr.q]
execute if score #q rpg_prh matches 0 run return 0
scoreboard players add @a[tag=rpg.pr.q] rpg_pr_qt 1
scoreboard players set #free rpg_prh 0
execute if score #state rpg_pr_i4 matches 0 if score #owe rpg_pr_i4 matches ..0 run scoreboard players set #free rpg_prh 4
execute if score #state rpg_pr_i3 matches 0 if score #owe rpg_pr_i3 matches ..0 run scoreboard players set #free rpg_prh 3
execute if score #state rpg_pr_i2 matches 0 if score #owe rpg_pr_i2 matches ..0 run scoreboard players set #free rpg_prh 2
execute if score #state rpg_pr_i1 matches 0 if score #owe rpg_pr_i1 matches ..0 run scoreboard players set #free rpg_prh 1
execute if score #free rpg_prh matches 0 as @a[tag=rpg.pr.q] run title @s actionbar {"text":"序章的战场都有人在打，空出来就轮到你…… All battlefields are busy.","color":"#E8D9B0"}
execute if score #free rpg_prh matches 0 run return 0
# 还有人在走开局（起名、抽身份、锻造教学）：多等一会儿，凑成一组
execute store result score #pend rpg_prh if entity @a[tag=rpg.ob,tag=!rpg.pr.q,tag=!rpg.pr]
scoreboard players set #go rpg_prh 0
execute if score #q rpg_prh matches 4.. run scoreboard players set #go rpg_prh 1
execute if score #pend rpg_prh matches 0 if entity @a[tag=rpg.pr.q,scores={rpg_pr_qt=3..}] run scoreboard players set #go rpg_prh 1
execute if entity @a[tag=rpg.pr.q,scores={rpg_pr_qt=60..}] run scoreboard players set #go rpg_prh 1
execute if score #go rpg_prh matches 0 as @a[tag=rpg.pr.q] run function rpg:prologue/wait_note
execute if score #go rpg_prh matches 0 run return 0
tag @a[tag=rpg.pr.q,limit=4] add rpg.pr.pick
execute if score #free rpg_prh matches 1 run function rpg:prologue/go_1
execute if score #free rpg_prh matches 2 run function rpg:prologue/go_2
execute if score #free rpg_prh matches 3 run function rpg:prologue/go_3
execute if score #free rpg_prh matches 4 run function rpg:prologue/go_4
