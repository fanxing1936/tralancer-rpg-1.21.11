# 晋入第 3 阶 · 光辉
scoreboard players set @s rpg_sef 3
scoreboard players add @s rpg_sp 1
function rpg:sephira/bonus/apply
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/soul
loot give @s loot rpg:forge/item/wash_gem
title @s times 10 60 20
title @s subtitle {"text":"Hod · הוד","color":"#FF8A4A","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"光辉","color":"#FF8A4A","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 0.88
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 3 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"光辉","color":"#FF8A4A","bold":true,"italic":false},{"text":"　生命 +4、技能点 +1、器胚 ×2、残魂 ×6、洗炼钻 ×1","color":"#E6DFCF","bold":false,"italic":false}]
