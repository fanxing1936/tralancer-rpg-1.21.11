kill @e[type=minecraft:marker,tag=rpg.ch1.slot1,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.slot2,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.slot3,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.slot1.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.slot2.label,distance=..72]
kill @e[type=minecraft:text_display,tag=rpg.ch1.slot3.label,distance=..72]
tag @s remove rpg.ch1.slot.1
tag @s remove rpg.ch1.slot.2
tag @s remove rpg.ch1.slot.3
tag @s add rpg.ch1.puzzle.wait.slot
scoreboard players add @s rpg_ch1_fail 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[错置回响] ","color":"#8B2500","bold":true,"italic":false},{"text":"器具与槽位含义冲突；击败回响后重新校准。","color":"gray","bold":false,"italic":false}]
execute positioned ^-8 ^ ^48 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 错置1","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
execute positioned ^8 ^ ^48 run summon minecraft:vex ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.puzzle.enemy","rpg.ch1.puzzle.enemy.current","rpg.ch1.puzzle.new"],life_ticks:1200,CustomName:["",{"text":"食名蝇 · 错置2","color":"#B5D957","bold":false,"italic":false}]}
scoreboard players operation @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] rpg_ch1_id = @s rpg_ch1_id
attribute @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] minecraft:max_health base set 18
data merge entity @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] {Health:18f}
tag @e[type=minecraft:vex,tag=rpg.ch1.puzzle.new,sort=nearest,limit=1] remove rpg.ch1.puzzle.new
