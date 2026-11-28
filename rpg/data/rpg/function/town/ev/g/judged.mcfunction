scoreboard players operation #v rpg_te = @s rpg_te_v
scoreboard players set @s rpg_te_v 0
scoreboard players add @a[tag=rpg.tw.in] rpg_ex_rites 1
execute if score #v rpg_te matches 1 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖裁决〗","color":"#C04A3C","bold":true,"italic":false},{"text":"  化身在圣火里烧尽了。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #v rpg_te matches 2 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖裁决〗","color":"#CDBE86","bold":true,"italic":false},{"text":"  化身被逐回了深渊。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #v rpg_te matches 3 run tellraw @a[tag=rpg.tw.in] ["",{"text":"〖裁决〗","color":"#4E9FAD","bold":true,"italic":false},{"text":"  化身被封进了图腾里。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #v rpg_te matches 4 run tellraw @s ["",{"text":"〖裁决〗","color":"#D596F2","bold":true,"italic":false},{"text":"  你悄悄松开了法阵的一角。它看了你一眼，化成蝇群散了。别人只看见它消失。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #v rpg_te matches 4 run scoreboard players add @s rpg_dm_rep 10
execute as @e[type=minecraft:vindicator,tag=rpg.te.av] at @s run particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.02 40
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  做得好。今晚镇上的人能睡个好觉了。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Well done. The town will sleep tonight.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr18 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
function rpg:town/ev/win
