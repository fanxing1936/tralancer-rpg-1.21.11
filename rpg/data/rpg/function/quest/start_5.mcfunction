# 接下支线：星辰拾荒者
execute if score @s rpg_q5 matches 1.. run return 0
scoreboard players set @s rpg_q5 1
scoreboard players set @s rpg_qc5 0
execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1
scoreboard players set @s rpg_q_mt 300
bossbar set rpg:quest_sub name ["",{"text":"〔支线・星辰拾荒者〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"完成 3 次坠星","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・星辰拾荒者〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔖𝔱𝔞𝔯𝔰𝔠𝔞𝔳𝔢𝔫𝔤𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  完成 3 次坠星","color":"#9C9A94","bold":false,"italic":false}]
