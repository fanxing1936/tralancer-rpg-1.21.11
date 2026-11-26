# 走完第 18 路径「战车」
scoreboard players set @s rpg_ps_18 4
scoreboard players add @s rpg_ex_xp 1920
give @s minecraft:paper[minecraft:item_model="rpg:paths/seal_18",minecraft:custom_name=["",{"text":"[路径]","color":"#D596F2","bold":true,"italic":false},{"text":"战车 · Cheth ח","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"第 18 路径　理解 — 严厉","color":"#9C9A94","bold":false,"italic":false},{"text":"走完这条路径的凭证","color":"#797979","bold":false,"italic":false},{"text":"正位：疾跑速度 +5%　逆位：疾跑中出手 +15%","color":"#797979","bold":false,"italic":false}],minecraft:custom_data={rpg_seal:18},minecraft:max_stack_size=1]
execute if score @s rpg_pillar matches 1 run scoreboard players add @s rpg_sp 1
title @s times 10 50 20
title @s subtitle {"text":"战车 · Cheth ח　—　理解 与 严厉","color":"#D48792","bold":false,"italic":false}
title @s title ["",{"text":"路径 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"战车","color":"#D48792","bold":true,"italic":false}]
playsound minecraft:block.end_portal_frame.fill master @s ~ ~ ~ 0.8 0.8
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.6 1.3
particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.04 30
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"走完了","color":"#9C9A94","bold":false,"italic":false},{"text":"第 18 路径「战车」","color":"#D48792","bold":true,"italic":false},{"text":"　阅历 +1920","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_pillar matches 1 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"路径碰到你的主柱：技能点 +1","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"翻开这张牌，选正位或逆位：","color":"#9C9A94","bold":false,"italic":false},{"text":"[择位]","color":"#C9A646","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pa_do set 18"},"hover_event":{"action":"show_text","value":{"text":"正位：疾跑速度 +5%\n逆位：疾跑中出手 +15%","color":"#E6DFCF","bold":false,"italic":false}}}]
