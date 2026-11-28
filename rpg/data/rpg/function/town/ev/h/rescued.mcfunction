tag @s remove rpg.te.taken
tag @s add rpg.te.saved
tellraw @a[distance=..12] ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"农妇","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔉𝔞𝔯𝔪𝔴𝔦𝔣𝔢","color":"#8F7430","italic":false},{"text":"  谢谢你，谢谢……我还以为再也见不到家了。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Thank you, thank you... I thought I'd never see home again.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.th01 voice @a[distance=..12] ~ ~ ~ 1 1
tellraw @a[distance=..12] ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"农夫","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔉𝔞𝔯𝔪𝔢𝔯","color":"#8F7430","italic":false},{"text":"  欠你一条命。有事说一声。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"I owe you my life. Just say the word.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.th02 voice @a[distance=..12] ~ ~ ~ 1 1
execute in minecraft:overworld as @e[type=minecraft:marker,tag=rpg.tw.at.spawn] if score @s rpg_tw_id = #run rpg_te at @s run tp @e[type=minecraft:villager,tag=rpg.te.saved] ~3 ~ ~2
tag @e[type=minecraft:villager,tag=rpg.te.saved] remove rpg.te.saved
