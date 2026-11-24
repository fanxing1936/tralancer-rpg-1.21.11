# 接下支线：玛门的账本
execute if score @s rpg_q4 matches 1.. run return 0
scoreboard players set @s rpg_q4 1
scoreboard players set @s rpg_qc4 0
execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1
scoreboard players set @s rpg_q_mt 300
bossbar set rpg:quest_sub name ["",{"text":"〔支线・玛门的账本〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"打死 3 只寻宝兔","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・玛门的账本〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔐𝔞𝔪𝔪𝔬𝔫'𝔰 𝔏𝔢𝔡𝔤𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  打死 3 只寻宝兔","color":"#9C9A94","bold":false,"italic":false}]
