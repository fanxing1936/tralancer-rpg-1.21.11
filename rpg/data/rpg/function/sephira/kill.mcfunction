# 锻造的三档击杀进度（rpg_fg_kx：1 普通 5 精英 50 Boss）顺路记阅历；Boss 的大头由胜利结算给
execute if score @s rpg_fg_kx matches 1 if score @s rpg_sef_dk matches ..299 run scoreboard players add @s rpg_ex_xp 1
execute if score @s rpg_fg_kx matches 1 run scoreboard players add @s rpg_sef_dk 1
execute if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_ex_xp 5
# 魔力：击杀 +4；圣力：杀死精英（恶魔、亡灵首领）+5
execute if score @s rpg_force matches 2 run scoreboard players add @s rpg_mana 4
execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana2 4
execute if score @s rpg_force matches 1 if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_mana 5
execute if score @s rpg_force matches 3 if score @s rpg_fg_kx matches 5.. run scoreboard players add @s rpg_mana 5
