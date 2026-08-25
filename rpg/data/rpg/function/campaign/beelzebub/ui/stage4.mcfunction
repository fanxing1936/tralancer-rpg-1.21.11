bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 run bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜痕迹 0 / 4","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 run bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜痕迹 1 / 4","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 run bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜痕迹 2 / 4","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 run bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜痕迹 3 / 4","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 4 run bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜痕迹 4 / 4","color":"#B5D957","bold":true,"italic":false}]
