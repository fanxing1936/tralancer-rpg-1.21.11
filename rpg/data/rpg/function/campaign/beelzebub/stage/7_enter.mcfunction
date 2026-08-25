bossbar set rpg:chapter1 value 58
bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅰ 镇压 · 见证三种权能","color":"#5A6B1E","bold":true,"italic":false}]
scoreboard players set @s rpg_ch1_seen 0
function rpg:campaign/beelzebub/spawn/boss
tellraw @a[tag=rpg.ch1.current] ["",{"text":"别西卜：","color":"#5A6B1E","bold":true,"italic":false},{"text":"可你们的账，一直都是平的。欢迎赴宴。","color":"#B5D957","bold":false,"italic":false}]
