scoreboard players operation #do rpg_xb = @s rpg_x_do
scoreboard players set @s rpg_x_do 0
execute if score #do rpg_xb matches 1 run function rpg:explore/page1
execute if score #do rpg_xb matches 2 run function rpg:explore/page2
execute if score #do rpg_xb matches 3 run function rpg:explore/page3
