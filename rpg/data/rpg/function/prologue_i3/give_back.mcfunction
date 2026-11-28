function rpg:prologue_i3/iso/restore
execute unless score @s rpg_pr_done matches 1.. run function rpg:prologue_i3/reward
scoreboard players set @s rpg_pr_done 1
