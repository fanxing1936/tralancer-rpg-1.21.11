tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  绳子断了，扶她走！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The ropes are cut, get her up!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew08 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#B8902F","bold":true,"italic":false},{"text":"审判官","color":"#B8902F","bold":true,"italic":false},{"text":"〗","color":"#B8902F","bold":true,"italic":false},{"text":" ℑ𝔫𝔮𝔲𝔦𝔰𝔦𝔱𝔬𝔯","color":"#8F7430","italic":false},{"text":"  犯人跑了！封住镇口！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The prisoner is loose! Seal the gates!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.iq03 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tag @a remove rpg.te.cut
scoreboard players set #ph rpg_te 3
scoreboard players set #tt rpg_te 0
bossbar set rpg:town_ev value 3
execute as @e[tag=rpg.te.inq] run data merge entity @s {NoAI:0b}
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  护送她到镇外林子里的营地。她走得慢，挡住后面追来的人。","color":"#9C9A94","bold":false,"italic":false}]
