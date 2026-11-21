# 命中管线之后：蓄势的空闲计数、本刻伤害清零。
execute if score @s rpg_fg_dd matches 1.. run scoreboard players set @s rpg_fg_idle 0
execute unless score @s rpg_fg_dd matches 1.. run scoreboard players add @s rpg_fg_idle 1
scoreboard players reset @s rpg_fg_dd
