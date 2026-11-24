execute if score @s rpg_pillar matches 1..3 run return 0
execute unless score @s rpg_sef matches 2.. run return 0
scoreboard players set @s rpg_pillar 1
function rpg:sephira/bonus/apply
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"主柱：","color":"#9C9A94","bold":false,"italic":false},{"text":"严厉柱","color":"#FF5A62","bold":true,"italic":false},{"text":"　进攻","color":"#9C9A94","bold":false,"italic":false}]
