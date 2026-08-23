summon minecraft:husk ~ ~ ~ {Tags:["rpg.sq.free","rpg.merc","rpg.sq.new"],IsBaby:0b,Silent:1b,PersistenceRequired:1b,CustomNameVisible:1b,CustomName:[{"text":"待雇 · ","color":"gray"},{"text":"HAIKU","color":"gray","bold":true}],Health:30f,attributes:[{id:"max_health",base:30f},{id:"attack_damage",base:1f},{id:"armor",base:1f},{id:"armor_toughness",base:0f},{id:"follow_range",base:0f},{id:"movement_speed",base:0f},{id:"knockback_resistance",base:0.3f}],equipment:{mainhand:{id:"minecraft:wooden_sword",count:1},head:{id:"minecraft:leather_helmet",count:1},chest:{id:"minecraft:leather_chestplate",count:1},legs:{id:"minecraft:leather_leggings",count:1},feet:{id:"minecraft:leather_boots",count:1}},drop_chances:{mainhand:1f,head:0f,chest:0f,legs:0f,feet:0f}}
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.sq.board","rpg.sq.newboard"],billboard:"center",alignment:"center",see_through:0b,background:1610612736,transformation:{translation:[0f,0.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f],right_rotation:[0f,0f,0f,1f]},text:[{"text":""}]}
execute as @e[type=minecraft:husk,tag=rpg.sq.new] run scoreboard players set @s rpg_sq_tier 1
# 信息板骑在他身上 —— 跟着走，不必每刻 tp，也就没有一刻的延迟
execute as @e[type=minecraft:text_display,tag=rpg.sq.newboard] run ride @s mount @e[type=minecraft:husk,tag=rpg.sq.new,limit=1,sort=nearest]
tag @e[type=minecraft:text_display,tag=rpg.sq.newboard] remove rpg.sq.newboard
# 信息板**下一刻**再画。装备是随 summon 一起给的，而它带来的属性修饰符
# 这一刻还没挂上 —— 现在读 armor 会少一截（实测 20，下一刻才是 30）。
tag @e[type=minecraft:husk,tag=rpg.sq.new] add rpg.sq.fresh
tag @e[type=minecraft:husk,tag=rpg.sq.new] remove rpg.sq.new
particle happy_villager ~ ~1 ~ 0.4 0.6 0.4 0.05 24
particle end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 12
