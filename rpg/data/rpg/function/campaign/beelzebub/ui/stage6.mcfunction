bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 0 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 1 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 2 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"准备仪式｜器具 3 / 3","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name ["",{"text":"仪式校准｜器具归入三槽","color":"#D4AF37","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name ["",{"text":"入场复盘｜三环已经闭合","color":"#B8A98B","bold":true,"italic":false}]
