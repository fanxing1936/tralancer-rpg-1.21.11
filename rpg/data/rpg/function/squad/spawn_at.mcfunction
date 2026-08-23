summon minecraft:husk ~ ~ ~ {Tags:["rpg.squad","rpg.sq.new"],IsBaby:0b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"佣兵","color":"#8FA1B3"}],Health:40f,attributes:[{id:"max_health",base:40f},{id:"attack_damage",base:4f},{id:"armor",base:4f},{id:"follow_range",base:0f},{id:"movement_speed",base:0f},{id:"knockback_resistance",base:0.3f}],drop_chances:{mainhand:1f}}
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players operation @s rpg_squad = #sq rpg_squad
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_mode 0
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_cd 0
tag @e[type=minecraft:husk,tag=rpg.sq.new] remove rpg.sq.new
particle happy_villager ~ ~1 ~ 0.4 0.6 0.4 0.05 30
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 16
