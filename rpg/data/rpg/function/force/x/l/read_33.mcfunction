advancement revoke @s only rpg:force/legacy_33
execute unless score @s rpg_force matches 1.. run return run function rpg:force/x/l/back_33
execute if score @s rpg_k33 matches 1.. run return run function rpg:force/x/l/known_33
scoreboard players set @s rpg_k33 1
execute if score @s rpg_force matches 1 run function rpg:force/x/l/auto1_33
execute if score @s rpg_force matches 3 run function rpg:force/x/l/auto1_33
execute if score @s rpg_force matches 2 run function rpg:force/x/l/auto2_33
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 0.8
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4
particle minecraft:enchant ~ ~1.2 ~ 0.5 0.8 0.5 0.6 60
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"读懂了","color":"#9C9A94","bold":false,"italic":false},{"text":"雅克","color":"#D8D2C4","bold":true,"italic":false},{"text":"的传承：","color":"#9C9A94","bold":false,"italic":false},{"text":"圣殿誓约","color":"#C9A646","bold":true,"italic":false},{"text":"。在技能页「王冠 · 传承」里把它放进槽。","color":"#E6DFCF","bold":false,"italic":false}]
