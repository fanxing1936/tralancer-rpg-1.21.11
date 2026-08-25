tag @e[type=minecraft:vindicator,tag=rpg.demon.minion.lord4,scores={rpg_mn_role=1},distance=..4] add rpg.ch1.preexisting
function rpg:minion/summon/beelzebub/zepar
tag @e[type=minecraft:vindicator,tag=rpg.demon.minion.lord4,tag=!rpg.ch1.preexisting,scores={rpg_mn_role=1},distance=..4,sort=nearest,limit=1] add rpg.ch1.minion.new
scoreboard players operation @e[tag=rpg.ch1.minion.new,limit=1] rpg_ch1_id = @s rpg_ch1_id
tag @e[tag=rpg.ch1.minion.new,limit=1] add rpg.ch1.minion
execute if entity @e[tag=rpg.ch1.minion.new,limit=1] run scoreboard players add @s rpg_ch1_obj 1
execute as @e[tag=rpg.ch1.minion.new,limit=1] run function rpg:campaign/beelzebub/minion/scale
tag @e[tag=rpg.ch1.minion.new] remove rpg.ch1.minion.new
tag @e[tag=rpg.ch1.preexisting] remove rpg.ch1.preexisting
