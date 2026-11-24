scoreboard players operation @s rpg_pl_fort = #d rpg_pl
execute if entity @e[tag=rpg.pl.b.castellan,distance=..64] run return 0
# 堡垒悬在一百格高处：就落在玩家身前两格，别掉下去
execute rotated ~ 0 positioned ^ ^ ^2 run function rpg:pl/fortress/castellan
tellraw @a[distance=..64] ["",{"text":"〖失乐园・堡主〗","color":"#E0483C","bold":true,"italic":false},{"text":" ℭ𝔞𝔰𝔱𝔢𝔩𝔩𝔞𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  黑石堡垒的主人听见了脚步声。","color":"#9C9A94","bold":false,"italic":false}]
