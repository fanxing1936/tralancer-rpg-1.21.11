# 晋入第 5 阶 · 美丽
scoreboard players set @s rpg_sef 5
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
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/rune_any
title @s times 10 60 20
title @s subtitle {"text":"Tiphareth · תפארת","color":"#FFD85A","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"美丽","color":"#FFD85A","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 1.00
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 5 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"美丽","color":"#FFD85A","bold":true,"italic":false},{"text":"　生命 +4、技能点 +2、器胚 ×4、残魂 ×10、洗炼钻 ×2、随机符文 ×1、技能可升到 2 级","color":"#E6DFCF","bold":false,"italic":false}]
execute if score @s rpg_force matches 0 run function rpg:sephira/force/awaken_ask
