kill @e[type=minecraft:marker,tag=rpg.ch1.route1,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.route2,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.route3,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.route1.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.route2.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.route3.label,distance=..72]
scoreboard players set @s rpg_ch1_choice 0
tag @s add rpg.ch1.puzzle.wait.route
scoreboard players add @s rpg_ch1_fail 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[伪序反噬] ","color":"#8B2500","bold":true,"italic":false},{"text":"错误因果唤来食名蝇；击败它们后重新排序。","color":"gray","bold":false,"italic":false}]
execute positioned ^-7 ^ ^43 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 伪序1","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
execute positioned ^7 ^ ^43 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 伪序2","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
