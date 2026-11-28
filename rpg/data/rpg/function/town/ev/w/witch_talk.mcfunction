execute unless score #run rpg_te matches 1.. run return 0
execute if score #ph rpg_te matches 2 run tag @s add rpg.te.cut
execute if score #ph rpg_te matches 2 run title @s actionbar ["",{"text":"割绳子……站着别动","color":"#9C9A94","bold":false,"italic":false}]
