bossbar set rpg:chapter1 value 41
bossbar set rpg:chapter1 name ["",{"text":"调查真名与弱点｜排除 2 个错误答案","color":"#5A6B1E","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[待验证假说] ","color":"#B8A98B","bold":true,"italic":false},{"text":"A 疫病复生　B 人为盗粮　C 暴食寄生。每项证物都必须能反驳至少一个解释。","color":"gray","bold":false,"italic":false}]
execute positioned ^-7 ^ ^31 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.hyp1","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^-7 ^ ^31 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.hyp1.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"炉灰检材 · 火灾？","color":"#706B5E","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^7 ^ ^33 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.hyp2","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^7 ^ ^33 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.hyp2.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"蝇茧剖面 · 疫病？","color":"#B5D957","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^ ^ ^39 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.hyp3","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^ ^ ^39 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.hyp3.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"拒食残渣 · 弱点？","color":"#5A6B1E","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new

function rpg:campaign/beelzebub/ui/scene/stage5
