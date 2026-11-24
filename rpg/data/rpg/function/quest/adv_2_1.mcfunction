scoreboard players set @s rpg_q2 99
loot give @s loot rpg:world/sp/soil
loot give @s loot rpg:world/sp/soil
loot give @s loot rpg:world/sp/soil
bossbar set rpg:quest_sub name ["",{"text":"〔支线・守墓人〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"墓地安静下来了。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・守墓人〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔳𝔢𝔨𝔢𝔢𝔭𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  墓地安静下来了。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
