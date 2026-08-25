tag @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] add rpg.ch1.ui.phase3
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s times 5 25 10
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s title ["",{"text":"固　阵","color":"#62D9E8","bold":true,"italic":false}]
execute as @a[tag=rpg.ch1.member,tag=rpg.ch1.current] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run title @s subtitle ["",{"text":"让被吞去的名字回来","color":"#E4EA9B","bold":false,"italic":false}]
