advancement revoke @s only rpg:force/legacy_36
execute unless score @s rpg_force matches 1.. run return run function rpg:force/x/l/back_36
execute if score @s rpg_k36 matches 1.. run return run function rpg:force/x/l/known_36
scoreboard players set @s rpg_k36 1
execute if score @s rpg_force matches 1 run function rpg:force/x/l/auto1_36
execute if score @s rpg_force matches 3 run function rpg:force/x/l/auto1_36
execute if score @s rpg_force matches 2 run function rpg:force/x/l/auto2_36
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.8
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4
particle minecraft:enchant ~ ~1.2 ~ 0.5 0.8 0.5 0.6 60
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"读懂了","color":"#9C9A94","bold":false,"italic":false},{"text":"路西法","color":"#5FD68C","bold":true,"italic":false},{"text":"的传承：","color":"#9C9A94","bold":false,"italic":false},{"text":"晨星","color":"#C9A646","bold":true,"italic":false},{"text":"。在技能页「王冠 · 传承」里把它放进槽。","color":"#E6DFCF","bold":false,"italic":false}]
