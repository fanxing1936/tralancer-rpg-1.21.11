tag @s add rpg.seal.warn90
scoreboard players set @s rpg_rel_w 0
scoreboard players set @s rpg_rel_left 100
scoreboard players operation @s rpg_rel_left -= @s rpg_agit
tellraw @s ["",{"text":"[遗物临界] ","color":"#FF3300","bold":true,"italic":false},{"text":"距逃逸还差 ","color":"gray","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_rel_left"},"color":"#FF3300","bold":false,"italic":false},{"text":" 点！立即净化或压制。","color":"#FF3300","bold":false,"italic":false}]
