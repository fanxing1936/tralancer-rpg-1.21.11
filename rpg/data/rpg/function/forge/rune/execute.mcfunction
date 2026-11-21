execute store result score #hp rpg_fg run data get entity @s Health 100
execute store result score #mx rpg_fg run attribute @s minecraft:max_health get 100
scoreboard players operation #hp rpg_fg *= #4 rpg_fg
execute if score #hp rpg_fg < #mx rpg_fg run scoreboard players add #pct rpg_fg 40
execute if score #hp rpg_fg < #mx rpg_fg run particle minecraft:damage_indicator ~ ~1 ~ 0.2 0.3 0.2 0.1 4
