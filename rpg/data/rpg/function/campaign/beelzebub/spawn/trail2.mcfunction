execute positioned ^ ^ ^20 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.trail2","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new
execute positioned ^ ^ ^20 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.trail2.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.3f,text:["",{"text":"带血车辙 · 乙","color":"#B5D957","bold":true,"italic":false}]}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..96] remove rpg.ch1.new

function rpg:campaign/beelzebub/ui/scene/trail2
