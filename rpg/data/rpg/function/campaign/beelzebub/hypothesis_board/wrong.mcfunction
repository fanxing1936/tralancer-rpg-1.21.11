kill @e[type=minecraft:marker,tag=rpg.ch1.theory1,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.theory2,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.theory3,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.theory1.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.theory2.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.theory3.label,distance=..72]
tag @s remove rpg.ch1.theory.1
tag @s remove rpg.ch1.theory.2
tag @s add rpg.ch1.puzzle.wait.theory
scoreboard players add @s rpg_ch1_fail 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[伪证反噬] ","color":"#8B2500","bold":true,"italic":false},{"text":"你提前排除了核心假说。击败具象化的伪证后重新审判。","color":"gray","bold":false,"italic":false}]
execute positioned ^-8 ^ ^46 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 伪证1","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
execute positioned ^ ^ ^50 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 伪证2","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
execute positioned ^8 ^ ^46 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 伪证3","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
