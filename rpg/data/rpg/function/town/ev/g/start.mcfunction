function rpg:town/ev/title1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  粮仓出事了。跟我来，别碰任何发黑的东西。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Something's wrong in the granary. Follow me, and touch nothing that has gone black.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr09 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  跟着神父去粮仓：找出三处痕迹（右键）。","color":"#9C9A94","bold":false,"italic":false}]
bossbar set rpg:town_ev max 3
bossbar set rpg:town_ev value 0
scoreboard players set #ph rpg_te 1
scoreboard players set #found rpg_te 0
execute as @e[type=minecraft:marker,tag=rpg.tw.in.granary] if score @s rpg_tw_id = #run rpg_te at @s run execute positioned ~-6 ~ ~-5 run function rpg:town/ev/g/trace {n:1}
execute as @e[type=minecraft:marker,tag=rpg.tw.in.granary] if score @s rpg_tw_id = #run rpg_te at @s run execute positioned ~5 ~ ~-3 run function rpg:town/ev/g/trace {n:2}
execute as @e[type=minecraft:marker,tag=rpg.tw.in.granary] if score @s rpg_tw_id = #run rpg_te at @s run execute positioned ~0 ~ ~6 run function rpg:town/ev/g/trace {n:3}
