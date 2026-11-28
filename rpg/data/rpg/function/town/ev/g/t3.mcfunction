tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  这个印记……三道横，一只眼。我见过它。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"This mark... three bars and an eye. I've seen it before.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr12 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players add #found rpg_te 1
execute store result bossbar rpg:town_ev value run scoreboard players get #found rpg_te
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  找到了：地上的印记（3 / 3）","color":"#9C9A94","bold":false,"italic":false}]
