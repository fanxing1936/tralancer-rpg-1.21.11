# 清理这个村民的旧商人部件，保留原有交易数据与其他乘客。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.mer.model.part] run kill @s
tag @s add rpg.mer
tag @s remove rpg.mer.smith
tag @s remove rpg.mer.model.smith
tag @s remove rpg.mer.mystery
tag @s remove rpg.mer.model.mystery
tag @s remove rpg.mer.luxury
tag @s remove rpg.mer.model.luxury
tag @s remove rpg.mer.travel
tag @s remove rpg.mer.model.travel
tag @s add rpg.mer.luxury
tag @s add rpg.mer.model.luxury
data merge entity @s {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b}
effect give @s minecraft:invisibility infinite 0 true
# 同一个函数顺序执行生成与挂载，重叠放置的商人也各自拥有部件。
tag @e[type=minecraft:villager,tag=rpg.mer.model.dressing] remove rpg.mer.model.dressing
tag @s add rpg.mer.model.dressing
execute summon minecraft:item_display run function rpg:merchant_luxury/part/head
execute summon minecraft:item_display run function rpg:merchant_luxury/part/eyebrow
execute summon minecraft:item_display run function rpg:merchant_luxury/part/r_eyepupil
execute summon minecraft:item_display run function rpg:merchant_luxury/part/r_eyeiris
execute summon minecraft:item_display run function rpg:merchant_luxury/part/l_eyepupil
execute summon minecraft:item_display run function rpg:merchant_luxury/part/l_eyeiris
execute summon minecraft:item_display run function rpg:merchant_luxury/part/mouth
execute summon minecraft:item_display run function rpg:merchant_luxury/part/nose
execute summon minecraft:item_display run function rpg:merchant_luxury/part/hatarmorlayer
execute summon minecraft:item_display run function rpg:merchant_luxury/part/hatarmorside
execute summon minecraft:item_display run function rpg:merchant_luxury/part/arm_l
execute summon minecraft:item_display run function rpg:merchant_luxury/part/arm_r
execute summon minecraft:item_display run function rpg:merchant_luxury/part/arm_m
execute summon minecraft:item_display run function rpg:merchant_luxury/part/body
execute summon minecraft:item_display run function rpg:merchant_luxury/part/tunic
execute summon minecraft:item_display run function rpg:merchant_luxury/part/leg_l
execute summon minecraft:item_display run function rpg:merchant_luxury/part/leg_r
tag @s remove rpg.mer.model.dressing
function rpg:merchant_luxury/anim/init
function rpg:merchant_luxury/anim/enter/idle
