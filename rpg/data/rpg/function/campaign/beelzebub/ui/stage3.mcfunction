bossbar set rpg:chapter1 color green
execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第一轮 · 封路与追猎","color":"#B7C84B","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第二轮 · 转运与伪记忆","color":"#B7C84B","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 3 run bossbar set rpg:chapter1 name ["",{"text":"罪仆战｜第三轮 · 处刑者","color":"#B7C84B","bold":true,"italic":false}]
execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 color red
execute if entity @s[tag=rpg.ch1.mira.captured] run bossbar set rpg:chapter1 name ["",{"text":"⚠ 救回米拉｜倒计时仍在推进","color":"#FF806B","bold":true,"italic":false}]
