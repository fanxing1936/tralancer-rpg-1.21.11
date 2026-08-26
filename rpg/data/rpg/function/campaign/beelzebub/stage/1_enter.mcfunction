bossbar set rpg:chapter1 value 8
bossbar set rpg:chapter1 name ["",{"text":"发现异常｜取得 3 份相互矛盾的记录","color":"#B8A98B","bold":true,"italic":false}]
execute positioned ^6 ^ ^5 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.anom1","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^6 ^ ^5 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.anom1.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"餐桌记录 · A","color":"#706B5E","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^-7 ^ ^9 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.anom2","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^-7 ^ ^9 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.anom2.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"死亡登记 · B","color":"#D4AF37","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^1 ^ ^15 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.anom3","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^1 ^ ^15 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.anom3.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"钟楼检材 · C","color":"#5A6B1E","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new

function rpg:campaign/beelzebub/ui/scene/stage1
