scoreboard players add @s task 1
execute as @s[scores={task=1}] at @s run tellraw @s ["你好，",{"text":"驱魔人","underlined":true,"bold":true,"color":"gold"}]
