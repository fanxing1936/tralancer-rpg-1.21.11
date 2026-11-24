# 右键生命树（as 玩家）：每天献一次
execute store result score #d rpg_pl run time query day
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"pl_fruit"}] run return run function rpg:pl/tree/fruit
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"pl_mud"}] run return run function rpg:pl/tree/mud
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rpg_mat:"pl_feather"}] run return run function rpg:pl/tree/feather
tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  枯死的生命树。手里拿着禁果、血泥或断羽再来，每天一次。","color":"#9C9A94","bold":false,"italic":false}]
