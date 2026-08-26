bossbar set rpg:chapter1 value 58
bossbar set rpg:chapter1 name ["",{"text":"万蝇腐宴｜Ⅰ 镇压 · 见证三种权能","color":"#5A6B1E","bold":true,"italic":false}]
scoreboard players set @s rpg_ch1_seen 0
function rpg:campaign/beelzebub/spawn/boss
tellraw @a[tag=rpg.ch1.current] ["",{"text":"卡西安：","color":"#D4AF37","bold":true,"italic":false},{"text":"登记人口，一万三千四百二十一。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"卡西安：","color":"#D4AF37","bold":true,"italic":false},{"text":"应发口粮，一万三千四百二十一。实发口粮，零。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"别西卜：","color":"#5A6B1E","bold":true,"italic":false},{"text":"可你们的账，一直都是平的。欢迎赴宴。","color":"#B5D957","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"先看祂怎样进食。我们需要证据，不只是伤口。","color":"gray","bold":false,"italic":false}]
