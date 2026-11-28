# 初见：侵蚀沙漠
tag @s add rpg.xb.eroded
scoreboard players add @s rpg_xb_n 1
scoreboard players set @s rpg_x_cd 12
title @s times 15 70 25
title @s title ["",{"text":"侵蚀沙漠","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"初见 · ","color":"#C9A646","bold":true,"italic":false},{"text":"危险 III","color":"#FFA15C","bold":true,"italic":false},{"text":" · 建议第 4 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔈𝔯𝔬𝔡𝔢𝔡 𝔇𝔢𝔰𝔢𝔯𝔱","color":"#8F7430","bold":false,"italic":false}]
tellraw @s ["",{"text":"　「风把沙漠一层层剥开，底下是更老的颜色。」","color":"#797979","bold":false,"italic":true,"hover_event":{"action":"show_text","value":{"text":"The wind peels the desert layer by layer, down to older colours.","color":"#8F7430","bold":false,"italic":false}}}]
playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1 0.7
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.8 0.84
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.6 1.12
playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.5 0.63
playsound rpg:vo.town.ex10 voice @s ~ ~ ~ 1 1
scoreboard players add @s rpg_x_pt 30
scoreboard players add @s rpg_ex_xp 30
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  侵蚀沙漠 记入见闻录　阅历 +30　探索点 +30","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_xb_n matches 19.. run function rpg:quest/title/get_traveler
