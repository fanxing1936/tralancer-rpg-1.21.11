# Per-mob roll for a skeleton variant (was 4 world-wide scans in rpg:command/tick).
execute store result score @s random run random value 1..20
execute if score @s random matches 10 run summon stray ~ ~ ~ {Tags:["skeleton"],Health:30,attributes:[{id:"max_health",base:30f}],equipment:{chest:{id:chainmail_chestplate,components:{trim:{pattern:wayfinder,material:lapis}},count:1},head:{id:chainmail_helmet,components:{trim:{pattern:eye,material:lapis}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f}}
execute if score @s random matches 11 run summon skeleton_horse ~ ~ ~ {Passengers:[{id:skeleton,Tags:["skeleton"],Health:30,attributes:[{id:"max_health",base:30f}],equipment:{chest:{id:iron_chestplate,components:{trim:{pattern:silence,material:quartz}},count:1},head:{id:iron_helmet,components:{trim:{pattern:silence,material:quartz}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f}}]}
execute if score @s random matches 12 run summon wither_skeleton ~ ~ ~ {Tags:["skeleton"],Health:40,attributes:[{id:"max_health",base:40f}],equipment:{chest:{id:netherite_chestplate,components:{trim:{pattern:silence,material:netherite}},count:1},head:{id:netherite_helmet,components:{trim:{pattern:silence,material:netherite}},count:1},mainhand:{id:netherite_sword,count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f}}


# 命中变种的掷点，原本那只让位 —— 图鉴写的是「直接替换成强化变种」，
# 而这里原本只是追加。不杀掉的话，一次生成会留下两只。
execute if score @s random matches 10 run kill @s
execute if score @s random matches 11 run kill @s
execute if score @s random matches 12 run kill @s