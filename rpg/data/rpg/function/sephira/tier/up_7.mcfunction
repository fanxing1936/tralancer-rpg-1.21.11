# 晋入第 7 阶 · 慈悲
scoreboard players set @s rpg_sef 7
scoreboard players add @s rpg_sp 2
function rpg:sephira/bonus/apply
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/stone_any
title @s times 10 60 20
title @s subtitle {"text":"Chesed · חסד","color":"#62B8F0","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"慈悲","color":"#62B8F0","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 1.12
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 7 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"慈悲","color":"#62B8F0","bold":true,"italic":false},{"text":"　生命 +4、技能点 +2、器胚 ×4、残魂 ×14、洗炼钻 ×2、随机符石 ×1、力条 +20","color":"#E6DFCF","bold":false,"italic":false}]
