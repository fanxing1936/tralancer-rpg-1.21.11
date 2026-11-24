scoreboard players set @s rpg_q3 99
loot give @s loot rpg:world/sp/bronze
loot give @s loot rpg:world/sp/bronze
loot give @s loot rpg:world/sp/bronze
function rpg:world/kab/line_6
bossbar set rpg:quest_sub name ["",{"text":"〔支线・圣卫的遗言〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"他们守着的，原来是这个。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・圣卫的遗言〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔏𝔞𝔰𝔱 𝔚𝔬𝔯𝔡𝔰 𝔬𝔣 𝔱𝔥𝔢 𝔊𝔲𝔞𝔯𝔡","color":"#8F7430","bold":false,"italic":false},{"text":"  他们守着的，原来是这个。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
