# 晋入第 9 阶 · 智慧
scoreboard players set @s rpg_sef 9
scoreboard players add @s rpg_sp 2
function rpg:sephira/bonus/apply
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
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
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/rune_any
loot give @s loot rpg:forge/stone_any
title @s times 10 60 20
title @s subtitle {"text":"Chokmah · חכמה","color":"#C9CDD6","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"智慧","color":"#C9CDD6","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 1.24
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 9 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"智慧","color":"#C9CDD6","bold":true,"italic":false},{"text":"　生命 +4、技能点 +2、器胚 ×6、残魂 ×18、洗炼钻 ×3、随机符文 ×1、随机符石 ×1、力条 +20","color":"#E6DFCF","bold":false,"italic":false}]
