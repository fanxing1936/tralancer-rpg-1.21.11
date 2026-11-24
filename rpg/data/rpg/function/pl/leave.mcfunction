execute unless data entity @s {Dimension:"rpg:paradise_lost"} run return run tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  你不在失乐园里。","color":"#9C9A94","bold":false,"italic":false}]
execute in rpg:paradise_lost if entity @s[x=0,y=83,z=0,distance=..36] run return run function rpg:pl/back
scoreboard players set @s rpg_pl_lv 5
execute store result score @s rpg_pl_px run data get entity @s Pos[0] 4
execute store result score @s rpg_pl_pz run data get entity @s Pos[2] 4
tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  站着别动，5 秒后离开。","color":"#9C9A94","bold":false,"italic":false}]
