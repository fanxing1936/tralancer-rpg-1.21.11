execute if score @s rpg_pillar matches 1..3 run return 0
execute unless score @s rpg_sef matches 2.. run return 0
scoreboard players set @s rpg_pillar 3
function rpg:sephira/bonus/apply
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"主柱：","color":"#9C9A94","bold":false,"italic":false},{"text":"中柱","color":"#FFD85A","bold":true,"italic":false},{"text":"　控制与机动","color":"#9C9A94","bold":false,"italic":false}]
