function rpg:prologue_i1/iso/restore
execute unless score @s rpg_pr_done matches 1.. run function rpg:prologue_i1/reward
scoreboard players set @s rpg_pr_done 1
