# 火墙（as/at 柱 i，朝柱 i+1）：沿墙每 1.3 格查一次，碰到的人烧 4
execute if score @s rpg_jq_id matches 0 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=1},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 1 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=2},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 2 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=3},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 3 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=4},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 4 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=5},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 5 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=6},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
execute if score @s rpg_jq_id matches 6 facing entity @e[type=minecraft:marker,tag=rpg.jqb.stake,scores={rpg_jq_id=0},limit=1] feet positioned ~ ~0.4 ~ run function rpg:jacques_boss/stakes/burn
