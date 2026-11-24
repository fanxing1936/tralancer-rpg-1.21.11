# 从原质页打开：魔力者翻到魔力树
execute unless score @s rpg_fo_pg matches 1..6 run scoreboard players set @s rpg_fo_pg 1
execute if score @s rpg_force matches 2 unless score @s rpg_fo_pg matches 4..6 run scoreboard players set @s rpg_fo_pg 4
function rpg:force/page/show
