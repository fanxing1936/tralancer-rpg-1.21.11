scoreboard players set #ok rpg_fo 0
function rpg:force/wash/near
execute unless score #ok rpg_fo matches 1 run return run function rpg:force/fail/say {m:"洗点要站在点燃的灵魂营火旁"}
execute store result score #n rpg_fo run clear @s *[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute unless score #n rpg_fo matches 5.. run return run function rpg:force/fail/say {m:"洗点要 5 个残魂"}
clear @s *[minecraft:custom_data~{rpg_mat:"soul"}] 5
function rpg:force/refund_h
function rpg:force/refund_m
playsound minecraft:block.soul_sand.break player @s ~ ~ ~ 1 0.6
particle minecraft:soul ~ ~1 ~ 0.4 0.6 0.4 0.03 30
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"洗点完成：花了 5 个残魂，两棵树的点都退回了。","color":"#E6DFCF","bold":false,"italic":false}]
