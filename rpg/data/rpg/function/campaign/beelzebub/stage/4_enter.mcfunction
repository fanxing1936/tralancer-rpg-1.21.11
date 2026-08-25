bossbar set rpg:chapter1 value 31
bossbar set rpg:chapter1 name ["",{"text":"确认活动区域｜追踪四处腐蝇痕迹","color":"#5A6B1E","bold":true,"italic":false}]
execute positioned ^ ^ ^12 run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.scene","rpg.ch1.point","rpg.ch1.trail1","rpg.ch1.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] remove rpg.ch1.new
execute positioned ^ ^ ^12 run summon minecraft:text_display ~ ~1.15 ~ {Tags:["rpg.ch1.scene","rpg.ch1.label","rpg.ch1.trail1.label","rpg.ch1.new"],billboard:"center",see_through:0b,shadow:1b,background:0,view_range:0.30f,text:"[\"\",{\"text\":\"腐蝇痕迹 1 / 4\",\"color\":\"#B5D957\",\"bold\":true,\"italic\":false}]"}
scoreboard players operation @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:text_display,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..80] remove rpg.ch1.new

function rpg:campaign/beelzebub/ui/scene/trail1
