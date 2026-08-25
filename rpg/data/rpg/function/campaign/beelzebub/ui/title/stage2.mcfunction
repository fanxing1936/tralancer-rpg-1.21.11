tag @s add rpg.ch1.ui.title.2
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s times 15 55 20
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s title ["",{"text":"异常显形","color":"#62D9E8","bold":true,"italic":false}]
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s subtitle ["",{"text":"她记得姓名，却失去了自己","color":"#706B5E","bold":false,"italic":false}]
