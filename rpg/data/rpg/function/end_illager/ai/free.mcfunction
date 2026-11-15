scoreboard players set @s rpg_ei_st 0
scoreboard players set @s rpg_ei_cd 70
execute if score @s rpg_ei_hc matches ..0 run scoreboard players set @s rpg_ei_hc 240
data merge entity @s {NoAI:0b}
