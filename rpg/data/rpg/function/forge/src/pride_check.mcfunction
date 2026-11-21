execute store result score #hp rpg_fg run data get entity @s Health 100
execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100
execute if score #hp rpg_fg >= #mx rpg_fg run scoreboard players add #spct rpg_fg 30
