scoreboard players set @s rpg_q4 99
loot give @s loot rpg:world/sin_shard_7
loot give @s loot rpg:world/sin_shard_7
loot give @s loot rpg:world/sin_shard_7
loot give @s loot rpg:world/sin_shard_7
bossbar set rpg:quest_sub name ["",{"text":"〔支线・玛门的账本〕 ","color":"#D4AF37","bold":true,"italic":false},{"text":"账平了。玛门记住了你的名字。","color":"#E6DFCF","bold":false,"italic":false}]
bossbar set rpg:quest_sub players @s
scoreboard players set @s rpg_q_st 80
tellraw @s ["",{"text":"〔支线・玛门的账本〕","color":"#D4AF37","bold":true,"italic":false},{"text":" 𝔐𝔞𝔪𝔪𝔬𝔫'𝔰 𝔏𝔢𝔡𝔤𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  账平了。玛门记住了你的名字。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
