tag @s add rpg.ch1.ui.title.9
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s times 15 55 20
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s title ["",{"text":"最后的见证人","color":"#FFF2A8","bold":true,"italic":false}]
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s subtitle ["",{"text":"米拉还记得自己的名字","color":"#B8A98B","bold":false,"italic":false}]
