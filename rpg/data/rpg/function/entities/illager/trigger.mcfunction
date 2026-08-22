execute as @e[name=fangs] at @s unless block ^ ^ ^0.5 #minecraft:air run tp @s ~ ~ ~ ~100 0
execute as @e[name=fangs] at @s if block ^ ^ ^0.5 #minecraft:air run tp @s ^ ^ ^0.3
execute as @e[name=fangs] at @s run scoreboard players add @s green 2
execute as @e[name=fangs,scores={green=10}] at @s run summon evoker_fangs ~ ~ ~ {Glowing:1b,Silent:1b}
execute as @e[name=fangs,scores={green=10}] at @s run scoreboard players set @s green 0

execute as @e[team=green] at @s if entity @e[distance=..1,type=minecraft:evoker_fangs] run effect give @s minecraft:resistance 1 255 true