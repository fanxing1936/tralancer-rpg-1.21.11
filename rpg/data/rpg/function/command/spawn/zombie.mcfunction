# Per-mob roll for a zombie variant (was 6 world-wide scans in rpg:command/tick).
execute store result score @s random run random value 1..20
execute if score @s random matches 8 run summon zombie ~ ~ ~ {Tags:["zombie"],Health:50,attributes:[{id:"attack_damage",base:4f},{id:"scale",base:1.1f},{id:"max_health",base:50f}],equipment:{chest:{id:chainmail_chestplate,components:{trim:{pattern:eye,material:redstone}},count:1},head:{id:target,count:1},mainhand:{id:iron_sword,count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}
execute if score @s random matches 9 run summon zombie ~ ~ ~ {Tags:["zombie"],Health:40,attributes:[{id:"attack_damage",base:2f},{id:"armor",base:5f},{id:"max_health",base:40f}],Passengers:[{id:zombie,Tags:["zombie"],IsBaby:1}],equipment:{chest:{id:leather_chestplate,components:{trim:{pattern:silence,material:copper},dyed_color:4673362},count:1},head:{id:mangrove_roots,count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f}}
execute if score @s random matches 10 run summon zombie_villager ~ ~ ~ {Tags:["zombie"],VillagerData:{type:plains,profession:armorer,level:5},Health:40,attributes:[{id:"attack_damage",base:2f},{id:"armor",base:5f},{id:"max_health",base:40f}],Passengers:[{id:zombie_villager,Tags:["zombie"],VillagerData:{type:plains,profession:farmer,level:2},IsBaby:1}],equipment:{chest:{id:chainmail_chestplate,components:{trim:{pattern:ward,material:quartz}},count:1},head:{id:cobweb,count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f}}
execute if score @s random matches 14..15 run summon zombie ~ ~ ~ {Tags:["zombie"],Passengers:[{id:zombie,Tags:["zombie"],Passengers:[{id:zombie,Tags:["zombie"],Passengers:[{id:zombie,Tags:["zombie"],Passengers:[{id:zombie,Tags:["zombie"]}]}]}]}]}
execute if score @s random matches 10 run summon zombie ~ ~ ~ {Tags:["zombie"],Health:100,attributes:[{id:"scale",base:3f},{id:"attack_damage",base:5f},{id:"attack_speed",base:1f},{id:"max_health",base:100f}]}


# 命中变种的掷点，原本那只让位 —— 图鉴写的是「直接替换成强化变种」，
# 而这里原本只是追加。不杀掉的话，一次生成会留下两只。
execute if score @s random matches 8 run kill @s
execute if score @s random matches 9 run kill @s
execute if score @s random matches 10 run kill @s
execute if score @s random matches 14..15 run kill @s