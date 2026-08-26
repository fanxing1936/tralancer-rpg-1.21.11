scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_time 0
bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅰ 镇压 · 见证三种权能","color":"#5A6B1E","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[Boss 战开始] ","color":"#8B2500","bold":true,"italic":false},{"text":"万蝇离席，腐宴开幕。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/spawn/boss
