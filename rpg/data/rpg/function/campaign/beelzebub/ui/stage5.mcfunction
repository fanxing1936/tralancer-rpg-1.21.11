bossbar set rpg:chapter1 color yellow
execute if score @s rpg_ch1_obj matches 0 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 0 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 1 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 1 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 2 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 2 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_obj matches 3 if score @s rpg_ch1_sub matches 0 run bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜假说 3 / 3","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 1 run bossbar set rpg:chapter1 name ["",{"text":"假说审判｜排除两个伪解","color":"#B5D957","bold":true,"italic":false}]
execute if score @s rpg_ch1_sub matches 2 run bossbar set rpg:chapter1 name ["",{"text":"案情复盘｜保留暴食寄生","color":"#B8A98B","bold":true,"italic":false}]
