tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  是蝇王。别西卜的一个化身。它不是全力，但足够吃空一个镇子。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"It's the Lord of Flies. An avatar of Beelzebub. Not his full strength, but enough to eat a town hollow.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr13 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  图腾立在门口。用圣水点燃它，法阵才会亮。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Set the totem at the door. Light it with holy water, or the circle won't wake.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr14 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
execute as @a[tag=rpg.tw.in] run function rpg:alc/give/totem
execute as @a[tag=rpg.tw.in] run function rpg:alc/give/holy
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  在粮仓门口立图腾（拿着驱魔图腾右键法阵），再扔驱魔圣水点燃它。","color":"#9C9A94","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.tw.at.granary] if score @s rpg_tw_id = #run rpg_te at @s run summon minecraft:interaction ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.circle","rpg.te.trace"],width:3f,height:0.6f,response:1b}
execute as @e[type=minecraft:marker,tag=rpg.tw.at.granary] if score @s rpg_tw_id = #run rpg_te at @s run summon minecraft:marker ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.cm"]}
scoreboard players set #ph rpg_te 2
scoreboard players set #totem rpg_te 0
