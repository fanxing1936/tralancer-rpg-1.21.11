bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 run bossbar set rpg:chapter1 name ["",{"text":"发现异常｜痕迹 0 / 3","color":"#B8A98B","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 run bossbar set rpg:chapter1 name ["",{"text":"发现异常｜痕迹 1 / 3","color":"#B8A98B","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 run bossbar set rpg:chapter1 name ["",{"text":"发现异常｜痕迹 2 / 3","color":"#B8A98B","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 run bossbar set rpg:chapter1 name ["",{"text":"发现异常｜痕迹 3 / 3","color":"#B8A98B","bold":true,"italic":false}]
