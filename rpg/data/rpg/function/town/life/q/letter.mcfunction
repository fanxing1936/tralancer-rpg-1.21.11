execute if items entity @s container.* minecraft:paper[minecraft:custom_data~{rpg_letter:1b}] run return run function rpg:town/life/q/letter_hand
execute if score @s rpg_tl_qd7 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"〖","color":"#C9B27A","bold":true,"italic":false},{"text":"村长","color":"#C9B27A","bold":true,"italic":false},{"text":"〗","color":"#C9B27A","bold":true,"italic":false},{"text":" 𝔈𝔩𝔡𝔢𝔯","color":"#8F7430","italic":false},{"text":"  这封信得送到邻镇去。路远，带上地图。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"This letter must reach the next town. It's a long road; take a map.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.el09 voice @s ~ ~ ~ 1 1
execute store result storage rpg:town q.t int 1 run scoreboard players get #t rpg_tl
function rpg:town/life/q/letter_give with storage rpg:town q
scoreboard players set @s rpg_tl_q7 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  寄往邻镇的信","color":"#E6DFCF","bold":true,"italic":false},{"text":"　把信交给另一座镇的村长","color":"#9C9A94","bold":false,"italic":false}]
