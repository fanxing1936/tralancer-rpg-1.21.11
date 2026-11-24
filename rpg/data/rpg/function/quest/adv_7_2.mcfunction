scoreboard players set @s rpg_q7 3
scoreboard players set @s rpg_qc7 0
bossbar set rpg:quest_sub name ["",{"text":"〔支线・失乐园〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"打倒基路伯","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・失乐园〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  打倒基路伯","color":"#9C9A94","bold":false,"italic":false}]
