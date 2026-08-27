execute unless entity @s[type=minecraft:player] run return 0
function rpg:prayer/currency
execute store result score @s rpg_pr_have run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
tellraw @s ["",{"text":"+------ 圣所祷告 · 耶和华 ------+","color":"#D4AF37","bold":true,"italic":false}]
tellraw @s ["",{"text":"奉上货币，静候恩赐。","color":"#AAB4C3","bold":false,"italic":false}]
tellraw @s ["",{"text":"持有 ","color":"#AAB4C3","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_pr_have"},"color":"#FFF2A8","bold":false,"italic":false},{"text":" 枚  ·  一次祷告 10 枚","color":"#AAB4C3","bold":false,"italic":false}]
tellraw @s ["",{"text":"[祷告一次]","color":"#FFD85A","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pray set 2"}},{"text":"  ","color":"#AAB4C3","bold":false,"italic":false},{"text":"[奖池与概率]","color":"#62D9E8","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pray set 3"}},{"text":"  ","color":"#AAB4C3","bold":false,"italic":false},{"text":"[返回面板]","color":"#AAB4C3","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 8"}}]
execute if score @s rpg_pr_pending matches 1.. run tellraw @s ["",{"text":"[领取待领恩赐]","color":"#FFF2A8","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pray set 4"}},{"text":"  已扣费的奖品不再收费。","color":"#AAB4C3","bold":false,"italic":false}]
tellraw @s ["",{"text":"普通粗金不计入货币；固定概率，无保底，可重复获得。","color":"#AAB4C3","bold":false,"italic":false}]
tellraw @s ["",{"text":"+--------------------------+","color":"#D4AF37","bold":true,"italic":false}]
