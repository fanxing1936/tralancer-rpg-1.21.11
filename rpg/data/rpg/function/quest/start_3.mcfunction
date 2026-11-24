# 接下支线：圣卫的遗言
execute if score @s rpg_q3 matches 1.. run return 0
scoreboard players set @s rpg_q3 1
scoreboard players set @s rpg_qc3 0
execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1
scoreboard players set @s rpg_q_mt 300
bossbar set rpg:quest_sub name ["",{"text":"〔支线・圣卫的遗言〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"打倒 3 名圣卫","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・圣卫的遗言〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔏𝔞𝔰𝔱 𝔚𝔬𝔯𝔡𝔰 𝔬𝔣 𝔱𝔥𝔢 𝔊𝔲𝔞𝔯𝔡","color":"#8F7430","bold":false,"italic":false},{"text":"  打倒 3 名圣卫","color":"#9C9A94","bold":false,"italic":false}]
