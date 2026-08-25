bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 0 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 1 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 2 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 3 / 3","color":"#D4AF37","bold":true,"italic":false}]
