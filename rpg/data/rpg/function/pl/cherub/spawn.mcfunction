# 在这名玩家附近落下（as/at 玩家）
summon minecraft:marker ~ ~ ~ {Tags:["rpg.pl.cm"]}
spreadplayers ~ ~ 4 24 under 200 false @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1]
execute at @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1] run function rpg:royal_guard/summon
execute at @e[type=minecraft:marker,tag=rpg.pl.cm,limit=1] as @e[tag=rpg.rg,distance=..6,limit=1,sort=nearest] run function rpg:pl/cherub/make
kill @e[type=minecraft:marker,tag=rpg.pl.cm]
execute in rpg:paradise_lost positioned 0 83 0 run tellraw @a[distance=0..] ["",{"text":"〖失乐园・基路伯〗","color":"#E0483C","bold":true,"italic":false},{"text":" ℭ𝔥𝔢𝔯𝔲𝔟","color":"#8F7430","bold":false,"italic":false},{"text":"  四面转动的火焰的剑，落在了灰烬边境。","color":"#9C9A94","bold":false,"italic":false}]
