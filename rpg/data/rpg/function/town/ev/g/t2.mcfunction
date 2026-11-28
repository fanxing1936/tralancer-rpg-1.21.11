tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  麦子从里面烂了，外面还是金的。贪吃的东西就是这样吃的。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The grain rotted from the inside; the outside is still gold. That is how gluttony eats.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr11 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players add #found rpg_te 1
execute store result bossbar rpg:town_ev value run scoreboard players get #found rpg_te
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  找到了：腐烂的麦袋（2 / 3）","color":"#9C9A94","bold":false,"italic":false}]
