tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  苍蝇不会无缘无故聚成团。记下来，这是第一处。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Flies don't swarm for no reason. Note it; that's the first sign.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr10 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players add #found rpg_te 1
execute store result bossbar rpg:town_ev value run scoreboard players get #found rpg_te
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  找到了：苍蝇团（1 / 3）","color":"#9C9A94","bold":false,"italic":false}]
