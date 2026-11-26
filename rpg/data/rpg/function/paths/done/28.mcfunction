# 走完第 28 路径「星星」
scoreboard players set @s rpg_ps_28 4
scoreboard players add @s rpg_ex_xp 120
give @s minecraft:paper[minecraft:item_model="rpg:paths/seal_28",minecraft:custom_name=["",{"text":"[路径]","color":"#D596F2","bold":true,"italic":false},{"text":"星星 · Tzaddi צ","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"第 28 路径　胜利 — 基础","color":"#9C9A94","bold":false,"italic":false},{"text":"走完这条路径的凭证","color":"#797979","bold":false,"italic":false},{"text":"正位：水下呼吸更久、游得更快　逆位：跳跃 +10%","color":"#797979","bold":false,"italic":false}],minecraft:custom_data={rpg_seal:28},minecraft:max_stack_size=1]
execute if score @s rpg_pillar matches 2 run scoreboard players add @s rpg_sp 1
execute if score @s rpg_pillar matches 3 run scoreboard players add @s rpg_sp 1
title @s times 10 50 20
title @s subtitle {"text":"星星 · Tzaddi צ　—　胜利 与 基础","color":"#A2B8B1","bold":false,"italic":false}
title @s title ["",{"text":"路径 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"星星","color":"#A2B8B1","bold":true,"italic":false}]
playsound minecraft:block.end_portal_frame.fill master @s ~ ~ ~ 0.8 0.8
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.6 1.3
particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.04 30
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"走完了","color":"#9C9A94","bold":false,"italic":false},{"text":"第 28 路径「星星」","color":"#A2B8B1","bold":true,"italic":false},{"text":"　阅历 +120","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_pillar matches 2 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"路径碰到你的主柱：技能点 +1","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_pillar matches 3 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"路径碰到你的主柱：技能点 +1","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"翻开这张牌，选正位或逆位：","color":"#9C9A94","bold":false,"italic":false},{"text":"[择位]","color":"#C9A646","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pa_do set 28"},"hover_event":{"action":"show_text","value":{"text":"正位：水下呼吸更久、游得更快\n逆位：跳跃 +10%","color":"#E6DFCF","bold":false,"italic":false}}}]
