tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.ui.phase4
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s times 5 25 10
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s title ["",{"text":"选择裁决","color":"#D596F2","bold":true,"italic":false}]
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s subtitle ["",{"text":"四条判词都将留下代价","color":"#B8A98B","bold":false,"italic":false}]
