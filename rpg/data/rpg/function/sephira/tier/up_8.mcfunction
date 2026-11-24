# 晋入第 8 阶 · 理解
scoreboard players set @s rpg_sef 8
scoreboard players add @s rpg_sp 1
function rpg:sephira/bonus/apply
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
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/gild_leaf
loot give @s loot rpg:forge/item/gild_leaf
title @s times 10 60 20
title @s subtitle {"text":"Binah · בינה","color":"#AAB4C3","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"理解","color":"#AAB4C3","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 1.18
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 8 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"理解","color":"#AAB4C3","bold":true,"italic":false},{"text":"　生命 +4、技能点 +1、残魂 ×16、铸造之石 ×4、镀金箔 ×2、技能可升到 3 级","color":"#E6DFCF","bold":false,"italic":false}]
