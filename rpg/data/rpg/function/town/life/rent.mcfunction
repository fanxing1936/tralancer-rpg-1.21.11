# 租屋：声望 40 + 20 货币；复活点挪到租屋门口
function rpg:town/life/rep_get
execute if score #rep rpg_tl matches ..39 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  声望到 40，村长才肯把屋子租给你。","color":"#FF6B5E","bold":false,"italic":false}]
execute store result score #m rpg_tl run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute if score #m rpg_tl matches ..19 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  租金是 20 枚货币。","color":"#FF6B5E","bold":false,"italic":false}]
clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 20
tag @s add rpg.tl.me
tellraw @s ["",{"text":"〖","color":"#C9B27A","bold":true,"italic":false},{"text":"村长","color":"#C9B27A","bold":true,"italic":false},{"text":"〗","color":"#C9B27A","bold":true,"italic":false},{"text":" 𝔈𝔩𝔡𝔢𝔯","color":"#8F7430","italic":false},{"text":"  镇东头有间空屋。你要是愿意，租下来当个家吧。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"There's an empty house at the east end. Rent it as your home, if you like.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.el04 voice @s ~ ~ ~ 1 1
execute as @e[type=minecraft:marker,tag=rpg.tw.at.rent] if score @s rpg_tw_id = #t rpg_tl at @s run spawnpoint @p[tag=rpg.tl.me] ~ ~ ~
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  复活点挪到了你的屋子门口。","color":"#C9A646","bold":false,"italic":false}]
tag @s remove rpg.tl.me
