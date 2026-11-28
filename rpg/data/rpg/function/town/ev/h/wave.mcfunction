scoreboard players add #wave rpg_te 1
execute store result bossbar rpg:town_ev value run scoreboard players get #wave rpg_te
bossbar set rpg:town_ev name ["",{"text":"空缺者事件","color":"#A8B4C0","bold":true,"italic":false},{"text":"　三波防守","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players operation #k rpg_te = #np rpg_te
execute if score #wave rpg_te matches 1 run scoreboard players operation #k rpg_te *= #2 rpg_te
execute if score #wave rpg_te matches 2.. run scoreboard players operation #k rpg_te *= #3 rpg_te
scoreboard players add #k rpg_te 3
execute if score #wave rpg_te matches 2 run scoreboard players add #k rpg_te 2
execute if score #wave rpg_te matches 3 run scoreboard players add #k rpg_te 4
execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s rpg_tw_id = #run rpg_te at @s run function rpg:town/ev/h/spawn_n
execute if score #wave rpg_te matches 2 run function rpg:town/ev/h/drag
execute if score #wave rpg_te matches 3 run function rpg:town/ev/h/giant
execute if score #wave rpg_te matches 1 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#A8B4C0","bold":true,"italic":false},{"text":"  第一波。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #wave rpg_te matches 2 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#A8B4C0","bold":true,"italic":false},{"text":"  第二波：它们开始抓人了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #wave rpg_te matches 3 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#A8B4C0","bold":true,"italic":false},{"text":"  第三波。最后那个……在变大。","color":"#9C9A94","bold":false,"italic":false}]
