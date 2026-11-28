# 初见：平原
tag @s add rpg.xb.plains
scoreboard players add @s rpg_xb_n 1
scoreboard players set @s rpg_x_cd 12
title @s times 15 70 25
title @s title ["",{"text":"平原","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"初见 · ","color":"#C9A646","bold":true,"italic":false},{"text":"危险 I","color":"#70DB70","bold":true,"italic":false},{"text":" · 新手也能走  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔓𝔩𝔞𝔦𝔫𝔰","color":"#8F7430","bold":false,"italic":false}]
tellraw @s ["",{"text":"　「平原上的风一直吹，像在数还有多少人没有回家。」","color":"#797979","bold":false,"italic":true,"hover_event":{"action":"show_text","value":{"text":"The wind on the plains never stops, as if counting who has not come home.","color":"#8F7430","bold":false,"italic":false}}}]
playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1 0.7
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.8 0.84
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.6 1.12
playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.5 0.63
playsound rpg:vo.town.ex01 voice @s ~ ~ ~ 1 1
scoreboard players add @s rpg_x_pt 10
scoreboard players add @s rpg_ex_xp 10
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  平原 记入见闻录　阅历 +10　探索点 +10","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_xb_n matches 19.. run function rpg:quest/title/get_traveler
