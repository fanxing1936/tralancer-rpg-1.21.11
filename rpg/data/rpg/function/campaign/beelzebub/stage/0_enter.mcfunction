bossbar set rpg:chapter1 value 2
bossbar set rpg:chapter1 name ["",{"text":"楔子｜第十三声钟","color":"#B8A98B","bold":true,"italic":false}]
playsound minecraft:block.bell.use master @a[tag=rpg.ch1.current] ~ ~ ~ 0.7 0.55
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[征调令 · 维斯珀后方城]","color":"#D4AF37","bold":true,"italic":false},{"text":"　任务：核对粮册与死亡登记。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"战争已经打了一百年。前线吃人，后方负责忘记。","color":"#706B5E","bold":false,"italic":false}]
