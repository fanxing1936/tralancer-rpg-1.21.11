# 补发条。已经有寿命的不动（正规路径给的 12000 算数），
# 只有真的没有才按默认值补。
tag @s add rpg.advent.timed
execute unless score @s rpg_fall matches 1.. run scoreboard players set @s rpg_fall 12000
