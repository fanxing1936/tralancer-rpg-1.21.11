scoreboard players set @s rpg_q5 99
loot give @s loot rpg:world/bp/starry
bossbar set rpg:quest_sub name ["",{"text":"〔支线・星辰拾荒者〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"三颗星的残片拼成了一张图纸。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・星辰拾荒者〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔖𝔱𝔞𝔯𝔰𝔠𝔞𝔳𝔢𝔫𝔤𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  三颗星的残片拼成了一张图纸。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
