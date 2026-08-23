execute as @a[distance=..20] at @s run title @s title {"text":"\ue201\ue202\ue203"}
execute as @a[distance=..20] at @s run title @s subtitle ["",{"text":"地狱的宰相","color":"#999999","bold":true},{"text":"\uE009"}," 别西卜"]
execute as @a[distance=..20] at @s run effect give @s minecraft:blindness 5 10 true
execute as @a[distance=..20] at @s run playsound minecraft:boss1 player @s
execute as @a[distance=..20] at @s run playsound minecraft:entity.generic.explode player @s
summon vindicator ~ ~ ~ {Johnny:1,Health:1000,Tags:["devil2","boss"],attributes:[{id:"max_health",base:1000f}],equipment:{head:{id:white_banner,components:{banner_patterns:[{pattern:rhombus,color:cyan},{pattern:stripe_bottom,color:light_gray},{pattern:stripe_center,color:gray},{pattern:half_horizontal,color:light_gray},{pattern:stripe_middle,color:black},{pattern:half_horizontal,color:light_gray},{pattern:circle,color:light_gray},{pattern:border,color:black}]},count:1},mainhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1},offhand:{id:netherite_sword,components:{custom_model_data:{floats:[1110007.0f]}},count:1}},drop_chances:{feet:0f,legs:0f,chest:0f,head:0f,mainhand:0f,offhand:0f}}
# `bossbar ... players` 是赋值不是追加 —— 逐个玩家写，等于每人
# 轮流把名单覆盖成自己，最后只有一个人看得见血条。一次设整组。
bossbar set minecraft:devil players @a[distance=..20]
bossbar set minecraft:devil color blue
bossbar set minecraft:devil name {"text":"\ue201\ue202\ue203"}
