# 初见：巨大冰原
tag @s add rpg.xb.glacier
scoreboard players add @s rpg_xb_n 1
scoreboard players set @s rpg_x_cd 12
title @s times 15 70 25
title @s title ["",{"text":"巨大冰原","color":"#E6DFCF","bold":true,"italic":false}]
title @s subtitle ["",{"text":"初见 · ","color":"#C9A646","bold":true,"italic":false},{"text":"危险 IV","color":"#FF6B5E","bold":true,"italic":false},{"text":" · 建议第 5 阶  ","color":"#9C9A94","bold":false,"italic":false},{"text":"𝔊𝔩𝔞𝔠𝔦𝔢𝔯 𝔖𝔭𝔦𝔯𝔢𝔰","color":"#8F7430","bold":false,"italic":false}]
tellraw @s ["",{"text":"　「冰原上的尖塔一年长一寸，没有人知道它们要去哪里。」","color":"#797979","bold":false,"italic":true,"hover_event":{"action":"show_text","value":{"text":"The ice spires grow an inch a year. No one knows where they are going.","color":"#8F7430","bold":false,"italic":false}}}]
playsound minecraft:block.amethyst_block.resonate ambient @s ~ ~ ~ 1 0.7
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.8 0.84
playsound minecraft:block.note_block.chime ambient @s ~ ~ ~ 0.6 1.12
playsound minecraft:block.note_block.bell ambient @s ~ ~ ~ 0.5 0.63
playsound rpg:vo.town.ex14 voice @s ~ ~ ~ 1 1
scoreboard players add @s rpg_x_pt 40
scoreboard players add @s rpg_ex_xp 40
function rpg:explore/milestone
function rpg:events/bt/explore
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
tellraw @s ["",{"text":"〖见闻录〗","color":"#C9A646","bold":true,"italic":false},{"text":"  巨大冰原 记入见闻录　阅历 +40　探索点 +40","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_xb_n matches 19.. run function rpg:quest/title/get_traveler
