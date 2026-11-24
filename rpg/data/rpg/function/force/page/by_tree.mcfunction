# 从圣徽 / 罪印打开：翻到那棵树（已经在那棵树上就留在原来那一支）
execute if score #tree rpg_fo matches 1 unless score @s rpg_fo_pg matches 1..3 run scoreboard players set @s rpg_fo_pg 1
execute if score #tree rpg_fo matches 2 unless score @s rpg_fo_pg matches 4..6 run scoreboard players set @s rpg_fo_pg 4
function rpg:force/page/show
