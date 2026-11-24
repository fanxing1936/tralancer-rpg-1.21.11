scoreboard players set @s rpg_q6 99
function rpg:world/kab/line_5
scoreboard players add @s rpg_ex_xp 30
function rpg:quest/q6_core
bossbar set rpg:quest_sub name ["",{"text":"〔支线・空缺者的名字〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"叫得出名字，才算理解。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・空缺者的名字〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔑𝔞𝔪𝔢 𝔬𝔣 𝔱𝔥𝔢 𝔙𝔞𝔠𝔞𝔫𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  叫得出名字，才算理解。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
