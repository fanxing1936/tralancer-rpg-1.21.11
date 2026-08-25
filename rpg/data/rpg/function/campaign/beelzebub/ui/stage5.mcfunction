bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 0 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 1 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 2 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 3 / 3","color":"#B5D957","bold":true,"italic":false}]
