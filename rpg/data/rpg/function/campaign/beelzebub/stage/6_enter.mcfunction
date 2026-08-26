bossbar set rpg:chapter1 value 49
bossbar set rpg:chapter1 name ["",{"text":"被撕去的判词｜准备 3 组仪式器具","color":"#D4AF37","bold":true,"italic":false}]
execute positioned ^-10 ^ ^35 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.cache1","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^-10 ^ ^35 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.cache1.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"封印档案箱","color":"#D4AF37","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^10 ^ ^35 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.cache2","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^10 ^ ^35 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.cache2.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"圣器保管箱","color":"#FFF2A8","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^ ^ ^42 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.cache3","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^ ^ ^42 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.cache3.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"裁决器具箱","color":"#62D9E8","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
tellraw @a[tag=rpg.ch1.current] ["",{"text":"伊莱亚：","color":"#D4AF37","bold":true,"italic":false},{"text":"器具封条都是真的，可判词从七直接跳到九。","color":"gray","bold":false,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"米拉：","color":"#FFF2A8","bold":true,"italic":false},{"text":"先拿齐东西。等我们知道缺的是什么，再决定要不要相信它。","color":"gray","bold":false,"italic":false}]

function rpg:campaign/beelzebub/ui/scene/stage6
