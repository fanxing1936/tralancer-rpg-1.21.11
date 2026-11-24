execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_mana 40
execute if score @s rpg_force matches 3 run scoreboard players add @s rpg_mana 40
execute if score @s rpg_mana > @s rpg_mana_max run scoreboard players operation @s rpg_mana = @s rpg_mana_max
execute if score @s rpg_force matches 1 run scoreboard players add @s rpg_vital 15
execute if score @s rpg_vital matches 101.. run scoreboard players set @s rpg_vital 100
execute unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　你没有圣力，只觉得嘴里有点甜。","color":"#797979","bold":false,"italic":false}]
