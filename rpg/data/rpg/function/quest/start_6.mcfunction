# 接下支线：空缺者的名字
execute if score @s rpg_q6 matches 1.. run return 0
scoreboard players set @s rpg_q6 1
scoreboard players set @s rpg_qc6 0
execute at @s run playsound rpg:bgm.onboard_flow record @s ~ ~ ~ 0.6 1
scoreboard players set @s rpg_q_mt 300
bossbar set rpg:quest_sub name ["",{"text":"〔支线・空缺者的名字〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"完成一次驱魔裁决","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・空缺者的名字〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔑𝔞𝔪𝔢 𝔬𝔣 𝔱𝔥𝔢 𝔙𝔞𝔠𝔞𝔫𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  完成一次驱魔裁决","color":"#9C9A94","bold":false,"italic":false}]
