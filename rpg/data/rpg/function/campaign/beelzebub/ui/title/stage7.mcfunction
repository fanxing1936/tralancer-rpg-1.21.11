tag @s add rpg.ch1.ui.title.7
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s times 5 35 15
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s title ["",{"text":"万蝇腐宴","color":"#B7C84B","bold":true,"italic":false}]
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s subtitle ["",{"text":"别西卜 · 暴食","color":"#5A6B1E","bold":false,"italic":false}]
