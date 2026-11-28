# 登录（as 刚登录的玩家）：序章已经结束而他还挂着 rpg.pr，就把他还原
scoreboard players reset @s rpg_pr_lv
execute if entity @s[tag=rpg.pri1] unless score #state rpg_pr_i1 matches 1.. run function rpg:prologue_i1/iso/restore
execute if entity @s[tag=rpg.pri1] if score #state rpg_pr_i1 matches 3 run gamemode spectator @s
execute if entity @s[tag=rpg.pri1] if score #state rpg_pr_i1 matches 5..6 run gamemode spectator @s
execute if entity @s[tag=rpg.pri1] if score #state rpg_pr_i1 matches 8..9 run gamemode spectator @s
