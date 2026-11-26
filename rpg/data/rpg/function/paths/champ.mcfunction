# 杀了首领精英（as 玩家；接在 rpg:elite/kill/*_champion）
execute if score @s rpg_ps_27 matches 1 run scoreboard players set @s rpg_pa_27 1
execute if score @s rpg_ps_19 matches 1 unless items entity @s armor.chest * run scoreboard players set @s rpg_pa_19 1
execute if score @s rpg_ps_17 matches 1 run function rpg:paths/champ17
