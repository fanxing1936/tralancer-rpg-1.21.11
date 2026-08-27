effect give @s minecraft:slowness 11 0 true
execute if score @s rpg_agit matches 0..39 run effect give @e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] minecraft:slowness 11 0 true
execute if score @s rpg_agit matches 0..39 run effect give @e[tag=rpg.demon,distance=..8] minecraft:slowness 11 0 true
execute if score @s rpg_agit matches 0..39 run effect give @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] minecraft:slowness 11 0 true
execute if score @s rpg_agit matches 40..69 run effect give @e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 40..69 run effect give @e[tag=rpg.demon,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 40..69 run effect give @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 70..89 run effect give @e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 70..89 run effect give @e[tag=rpg.demon,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 70..89 run effect give @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] minecraft:slowness 11 1 true
execute if score @s rpg_agit matches 90..99 run effect give @e[type=#rpg:seal_hostile,type=!minecraft:player,tag=!rpg.demon,tag=!rpg.demon.minion,distance=..8] minecraft:slowness 11 2 true
execute if score @s rpg_agit matches 90..99 run effect give @e[tag=rpg.demon,distance=..8] minecraft:slowness 11 2 true
execute if score @s rpg_agit matches 90..99 run effect give @e[tag=rpg.demon.minion,tag=!rpg.demon,distance=..8] minecraft:slowness 11 2 true
scoreboard players add @s rpg_agit 3
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
