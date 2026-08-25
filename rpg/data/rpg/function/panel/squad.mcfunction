scoreboard players set #panel_count rpg_squad 0
scoreboard players operation #panel_squad rpg_squad = @s rpg_squad
execute if entity @s[tag=rpg.sq.lead] as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #panel_squad rpg_squad run scoreboard players add #panel_count rpg_squad 1
scoreboard players operation @s rpg_sq_n = #panel_count rpg_squad
tellraw @s ["",{"text":"+---------- 佣兵小队 ----------+","color":"#D4AF37","italic":false,"bold":true}]
execute unless entity @s[tag=rpg.sq.lead] run tellraw @s ["",{"text":"尚未建立佣兵编制。","color":"gray","italic":false}]
execute if entity @s[tag=rpg.sq.lead] run tellraw @s ["",{"text":"当前编制：","color":"gray","italic":false},{"score":{"name":"@s","objective":"rpg_sq_n"},"color":"#D4AF37","italic":false},{"text":" / 4","color":"dark_gray","italic":false}]
execute if entity @s[tag=rpg.sq.lead,scores={rpg_sq_stance=0}] run tellraw @s ["",{"text":"全队姿态：跟随","color":"#70DB70","italic":false}]
execute if entity @s[tag=rpg.sq.lead,scores={rpg_sq_stance=1}] run tellraw @s ["",{"text":"全队姿态：驻守","color":"#8FC7FF","italic":false}]
tellraw @s ["",{"text":"募兵旗：招募/晋升　指挥旗：集火/配装/姿态/解雇","color":"gray","italic":false}]
tellraw @s ["",{"text":"姿态切换：潜行 + 指挥旗长按右键","color":"dark_gray","italic":false}]
tellraw @s ["",{"text":"[返回面板]","color":"#D4AF37","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_panel set 8"}}]
