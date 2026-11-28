# 初见：火山
tag @s add rpg.xb.volcano
scoreboard players add @s rpg_xb_n 1
scoreboard players set @s rpg_x_cd 12
title @s times 15 70 25
title @s title ["",{"text":"火山","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"初见 · ","color":"#C9A646","bold":true,"italic":false},{"text":"危险 V","color":"#FF3300","bold":true,"italic":false},{"text":" · 建议第 6 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔙𝔬𝔩𝔠𝔞𝔫𝔬","color":"#8F7430","bold":false,"italic":false}]
tellraw @s ["",{"text":"　「大地在这里流血，流成了火。」","color":"#797979","bold":false,"italic":true,"hover_event":{"action":"show_text","value":{"text":"Here the land bleeds, and the blood is fire.","color":"#8F7430","bold":false,"italic":false}}}]
playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1 0.7
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.8 0.84
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.6 1.12
playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.5 0.63
playsound rpg:vo.town.ex16 voice @s ~ ~ ~ 1 1
scoreboard players add @s rpg_x_pt 50
scoreboard players add @s rpg_ex_xp 50
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  火山 记入见闻录　阅历 +50　探索点 +50","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_xb_n matches 19.. run function rpg:quest/title/get_traveler
