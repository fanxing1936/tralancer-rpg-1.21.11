# 晋入第 2 阶 · 基础
scoreboard players set @s rpg_sef 2
scoreboard players add @s rpg_sp 1
function rpg:sephira/bonus/apply
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
title @s times 10 60 20
title @s subtitle {"text":"Yesod · יסוד","color":"#D596F2","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"基础","color":"#D596F2","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 0.82
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 2 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"基础","color":"#D596F2","bold":true,"italic":false},{"text":"　生命 +4、技能点 +1、器胚 ×2、残魂 ×4","color":"#E6DFCF","bold":false,"italic":false}]
execute unless score @s rpg_pillar matches 1..3 run function rpg:sephira/pillar/ask
