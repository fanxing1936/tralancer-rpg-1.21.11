scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_ex_lvl 0
scoreboard players add @s rpg_ex_path 0
scoreboard players add @s rpg_ex_slots 0
function rpg:inquest/career/sync
tellraw @s ["",{"text":"+---------- 驱魔师档案 ----------+","color":"#FFF2A8","italic":false,"bold":true}]
tellraw @s ["",{"text":"阶位 ","color":"gray","italic":false},{"score":{"name":"@s","objective":"rpg_ex_lvl"},"color":"white","italic":false},{"text":"　阅历 ","color":"gray","italic":false},{"score":{"name":"@s","objective":"rpg_ex_xp"},"color":"#FFD85A","italic":false},{"text":"　仪式槽 ","color":"gray","italic":false},{"score":{"name":"@s","objective":"rpg_ex_slots"},"color":"#62D9E8","italic":false}]
execute if score @s rpg_ex_path matches 0 run tellraw @s ["",{"text":"选择道路　","color":"gray","italic":false},{"text":"[审判]","color":"#FF806B","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 21"}},{"text":"  ","color":"white","italic":false},{"text":"[守护]","color":"#8FC7FF","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 22"}},{"text":"  ","color":"white","italic":false},{"text":"[秘仪]","color":"#D596F2","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 23"}}]
execute if score @s rpg_ex_path matches 1 run tellraw @s ["",{"text":"审判之道","color":"#FF806B","italic":false,"bold":true},{"text":"　识破 · 打断 · 处决","color":"gray","italic":false}]
execute if score @s rpg_ex_path matches 2 run tellraw @s ["",{"text":"守护之道","color":"#8FC7FF","italic":false,"bold":true},{"text":"　固阵 · 减损 · 封印","color":"gray","italic":false}]
execute if score @s rpg_ex_path matches 3 run tellraw @s ["",{"text":"秘仪之道","color":"#D596F2","italic":false,"bold":true},{"text":"　净化 · 加速 · 通晓","color":"gray","italic":false}]
function rpg:inquest/career/claim
tellraw @s ["",{"text":"[返回面板]","color":"#D4AF37","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 8"}}]
