execute if score @s rpg_pl_tree = #d rpg_pl run return run tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  今天已经献过了。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players operation @s rpg_pl_tree = #d rpg_pl
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
attribute @s minecraft:max_health modifier remove rpg:pl_tree
attribute @s minecraft:max_health modifier add rpg:pl_tree 8 add_value
scoreboard players set @s rpg_pl_tb 3600
execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.02 60
playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 1.2
tellraw @s ["",{"text":"〖失乐园〗","color":"#E0483C","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  生命树收下了血泥：生命 +8，一小时。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:quest/hook/tree
