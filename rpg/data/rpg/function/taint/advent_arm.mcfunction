# 补发条。已经有寿命的不动（正规路径给的 600 / 2400 都算数），
# 只有真的没有才按默认值补。
tag @s add rpg.advent.timed
execute unless score @s rpg_fall matches 1.. run scoreboard players set @s rpg_fall 600
