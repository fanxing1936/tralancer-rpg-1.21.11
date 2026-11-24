# 晋入第 10 阶 · 王冠
scoreboard players set @s rpg_sef 10
scoreboard players add @s rpg_sp 2
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
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/gild_leaf
loot give @s loot rpg:forge/item/gild_leaf
loot give @s loot rpg:forge/item/gild_leaf
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
loot give @s loot rpg:forge/item/wash_gem
title @s times 10 60 20
title @s subtitle {"text":"Kether · כתר","color":"#FFF2A8","bold":false,"italic":true}
title @s title ["",{"text":"晋入 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"王冠","color":"#FFF2A8","bold":true,"italic":false}]
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.8 1.30
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.2
particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.05 40
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"晋入第 10 阶 ","color":"#9C9A94","bold":false,"italic":false},{"text":"王冠","color":"#FFF2A8","bold":true,"italic":false},{"text":"　生命 +4、技能点 +2、残魂 ×24、铸造之石 ×6、镀金箔 ×3、洗炼钻 ×3、终式解锁","color":"#E6DFCF","bold":false,"italic":false}]
