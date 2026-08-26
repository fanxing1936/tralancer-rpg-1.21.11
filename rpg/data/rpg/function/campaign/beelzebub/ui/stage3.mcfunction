execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"见证人封锁线｜听完简报后迎战","color":"#FFF2A8","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 1..3 run bossbar set rpg:chapter1 color green
execute if score @s rpg_ch1_sub matches 12..13 run bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_sub matches 12..13 run bossbar set rpg:chapter1 name ["",{"text":"战间复盘｜敌人暂未入场","color":"#B8A98B","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第一轮 · 封路与追猎","color":"#B7C84B","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第二轮 · 转运与伪记忆","color":"#B7C84B","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 3 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第三轮 · 处刑者","color":"#B7C84B","bold":true,"italic":false}]
execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 color red
execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 name ["",{"text":"⚠ 救回米拉｜倒计时仍在推进","color":"#FF806B","bold":true,"italic":false}]
