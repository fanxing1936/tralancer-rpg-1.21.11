summon minecraft:marker ~ ~1 ~ {Tags:["rpg.ch1.scene","rpg.ch1.ui.escape","rpg.ch1.ui.escape.new"]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.ui.escape.new,sort=nearest,limit=1,distance=..3] rpg_ch1_id = @s rpg_ch1_id
tag @e[type=minecraft:marker,tag=rpg.ch1.ui.escape.new,sort=nearest,limit=1,distance=..3] remove rpg.ch1.ui.escape.new
schedule function rpg:campaign/beelzebub/ui/escape/pulse1 2t replace
