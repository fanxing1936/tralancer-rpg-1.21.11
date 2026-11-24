# 登录（as 刚登录的玩家）：序章已经结束而他还挂着 rpg.pr，就把他还原
scoreboard players reset @s rpg_pr_lv
execute if entity @s[tag=rpg.pr] unless score #state rpg_pr matches 1.. run function rpg:prologue/iso/restore
execute if entity @s[tag=rpg.pr] if score #state rpg_pr matches 3 run gamemode spectator @s
execute if entity @s[tag=rpg.pr] if score #state rpg_pr matches 5..6 run gamemode spectator @s
execute if entity @s[tag=rpg.pr] if score #state rpg_pr matches 8..9 run gamemode spectator @s
