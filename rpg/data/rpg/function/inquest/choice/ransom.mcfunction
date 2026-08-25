execute if score @s rpg_ex_choice matches 11 if entity @s[level=3..] run return run function rpg:inquest/choice/ransom_xp
execute if score @s rpg_ex_choice matches 11 unless entity @s[level=3..] run tellraw @s ["",{"text":"[赎金失败] 需要至少 3 级经验。","color":"red","italic":false}]
execute if score @s rpg_ex_choice matches 12 if score @s health matches 9.. run return run function rpg:inquest/choice/ransom_hp
execute if score @s rpg_ex_choice matches 12 unless score @s health matches 9.. run tellraw @s ["",{"text":"[赎金失败] 生命不足以献出 4 颗心。","color":"red","italic":false}]
execute if score @s rpg_ex_choice matches 13 if items entity @s inventory.* minecraft:gold_ingot run return run function rpg:inquest/choice/ransom_gold
execute if score @s rpg_ex_choice matches 13 unless items entity @s inventory.* minecraft:gold_ingot run tellraw @s ["",{"text":"[赎金失败] 背包中没有金锭。","color":"red","italic":false}]
