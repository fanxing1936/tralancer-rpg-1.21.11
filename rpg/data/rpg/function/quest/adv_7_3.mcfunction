scoreboard players set @s rpg_q7 99
loot give @s loot rpg:world/bp_legend_any
bossbar set rpg:quest_sub name ["",{"text":"〔支线・失乐园〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"门还在那里，只是没有人再守着它。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・失乐园〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔓𝔞𝔯𝔞𝔡𝔦𝔰𝔢 𝔏𝔬𝔰𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  门还在那里，只是没有人再守着它。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
