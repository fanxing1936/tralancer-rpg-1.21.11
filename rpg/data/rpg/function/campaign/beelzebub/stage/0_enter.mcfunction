bossbar set rpg:chapter1 value 2
bossbar set rpg:chapter1 name ["",{"text":"序幕｜第十三声钟","color":"#B8A98B","bold":true,"italic":false}]
playsound minecraft:ambient.cave master @a[tag=rpg.ch1.current] ~ ~ ~ 0.55 0.72
tellraw @a[tag=rpg.ch1.current] ["",{"text":"战争已经打了一百年。前线吃人，后方负责忘记。","color":"#706B5E","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"书记员 伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"教廷说你没有听见第十三声钟。","color":"gray","bold":false,"italic":false}]
