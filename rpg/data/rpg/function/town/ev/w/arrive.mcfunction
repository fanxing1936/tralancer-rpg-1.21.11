tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  到了。这里他们找不到。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"We're here. They won't find us here.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew11 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players set #ph rpg_te 4
scoreboard players set #tt rpg_te 0
bossbar set rpg:town_ev value 4
execute as @e[tag=rpg.te.g] run function rpg:town/ev/remove
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  到了。坐下来听她讲。","color":"#9C9A94","bold":false,"italic":false}]
