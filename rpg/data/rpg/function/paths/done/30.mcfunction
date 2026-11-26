# 走完第 30 路径「太阳」
scoreboard players set @s rpg_ps_30 4
scoreboard players add @s rpg_ex_xp 60
give @s minecraft:paper[minecraft:item_model="rpg:paths/seal_30",minecraft:custom_name=["",{"text":"[路径]","color":"#D596F2","bold":true,"italic":false},{"text":"太阳 · Resh ר","color":"#FFFFFF","bold":false,"italic":false}],minecraft:lore=[{"text":"第 30 路径　光辉 — 基础","color":"#9C9A94","bold":false,"italic":false},{"text":"走完这条路径的凭证","color":"#797979","bold":false,"italic":false},{"text":"正位：白天每 10 秒回 1 生命　逆位：攻击速度 +3%","color":"#797979","bold":false,"italic":false}],minecraft:custom_data={rpg_seal:30},minecraft:max_stack_size=1]
execute if score @s rpg_pillar matches 1 run scoreboard players add @s rpg_sp 1
execute if score @s rpg_pillar matches 3 run scoreboard players add @s rpg_sp 1
title @s times 10 50 20
title @s subtitle {"text":"太阳 · Resh ר　—　光辉 与 基础","color":"#EA909E","bold":false,"italic":false}
title @s title ["",{"text":"路径 · ","color":"#9C9A94","bold":false,"italic":false},{"text":"太阳","color":"#EA909E","bold":true,"italic":false}]
playsound minecraft:block.end_portal_frame.fill master @s ~ ~ ~ 0.8 0.8
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.6 1.3
particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.04 30
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"走完了","color":"#9C9A94","bold":false,"italic":false},{"text":"第 30 路径「太阳」","color":"#EA909E","bold":true,"italic":false},{"text":"　阅历 +60","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_pillar matches 1 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"路径碰到你的主柱：技能点 +1","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_pillar matches 3 run tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"路径碰到你的主柱：技能点 +1","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"[路径] ","color":"#C9A646","bold":true,"italic":false},{"text":"翻开这张牌，选正位或逆位：","color":"#9C9A94","bold":false,"italic":false},{"text":"[择位]","color":"#C9A646","bold":true,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_pa_do set 30"},"hover_event":{"action":"show_text","value":{"text":"正位：白天每 10 秒回 1 生命\n逆位：攻击速度 +3%","color":"#E6DFCF","bold":false,"italic":false}}}]
