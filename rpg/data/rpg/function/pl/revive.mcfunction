# 死在失乐园里：复活后回到门内
scoreboard players set @s rpg_pl_dc 0
execute in rpg:paradise_lost run tp @s 0.5 88 17.5 180 0
effect give @s minecraft:weakness 30 1
tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  你在门里醒来。","color":"#9C9A94","bold":false,"italic":false}]
