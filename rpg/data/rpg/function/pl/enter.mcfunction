# 玩家面板「进入」
execute if data entity @s {Dimension:"rpg:paradise_lost"} run return run tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  你已经在失乐园里了。","color":"#9C9A94","bold":false,"italic":false}]
execute if entity @s[tag=rpg.pr] run return run tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  序章还没结束。","color":"#9C9A94","bold":false,"italic":false}]
execute store result storage rpg:paradise t.id int 1 run scoreboard players get @s rpg_fg_id
function rpg:pl/save with storage rpg:paradise t
execute unless score @s rpg_sef matches 2.. unless entity @s[tag=rpg.pl.ok] run return run function rpg:pl/warn
tag @s add rpg.pl.wait
execute if score #built rpg_pl matches 10 run return run function rpg:pl/go
execute unless score #built rpg_pl matches 1 run function rpg:pl/prepare
tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  门正在打开……","color":"#9C9A94","bold":false,"italic":false}]
