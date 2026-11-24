function rpg:prologue/iso/restore
execute unless score @s rpg_pr_done matches 1.. run function rpg:prologue/reward
scoreboard players set @s rpg_pr_done 1
