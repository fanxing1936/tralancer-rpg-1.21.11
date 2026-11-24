# 接下支线：失乐园
execute if score @s rpg_q7 matches 1.. run return 0
scoreboard players set @s rpg_q7 1
scoreboard players set @s rpg_qc7 0
execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1
scoreboard players set @s rpg_q_mt 300
bossbar set rpg:quest_sub name ["",{"text":"〔支线・失乐园〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"过比逊河庭","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・失乐园〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  过比逊河庭","color":"#9C9A94","bold":false,"italic":false}]
