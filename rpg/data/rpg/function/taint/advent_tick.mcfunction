# 降临者的寿命。场上没有这样的东西时，上层那道守卫会整段跳过。
scoreboard players remove @s rpg_fall 1
execute if entity @s[scores={rpg_fall=..0}] at @s run function rpg:taint/advent_gone
