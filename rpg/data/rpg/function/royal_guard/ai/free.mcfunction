scoreboard players set @s rpg_rg_st 0
scoreboard players set @s rpg_rg_cd 50
function rpg:royal_guard/anim/enter/idle
data merge entity @s {NoAI:0b}
