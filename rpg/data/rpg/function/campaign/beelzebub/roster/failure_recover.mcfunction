scoreboard players set @s rpg_ch1_empty 0
execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/recover_minions
execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/recover_boss
