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
tag @s add rpg.mer.smith
tag @s add rpg.mer.model.smith
data merge entity @s {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b}
effect give @s minecraft:invisibility infinite 0 true
# 同一个函数顺序执行生成与挂载，重叠放置的商人也各自拥有部件。
tag @e[type=minecraft:villager,tag=rpg.mer.model.dressing] remove rpg.mer.model.dressing
tag @s add rpg.mer.model.dressing
execute summon minecraft:item_display run function rpg:merchant_smith/part/head
execute summon minecraft:item_display run function rpg:merchant_smith/part/eyebrow
execute summon minecraft:item_display run function rpg:merchant_smith/part/r_eyepupil
execute summon minecraft:item_display run function rpg:merchant_smith/part/r_eyeiris
execute summon minecraft:item_display run function rpg:merchant_smith/part/l_eyepupil
execute summon minecraft:item_display run function rpg:merchant_smith/part/l_eyeiris
execute summon minecraft:item_display run function rpg:merchant_smith/part/mouth
execute summon minecraft:item_display run function rpg:merchant_smith/part/nose
execute summon minecraft:item_display run function rpg:merchant_smith/part/hatarmorlayer
execute summon minecraft:item_display run function rpg:merchant_smith/part/hatarmorside
execute summon minecraft:item_display run function rpg:merchant_smith/part/arm_l
execute summon minecraft:item_display run function rpg:merchant_smith/part/arm_r
execute summon minecraft:item_display run function rpg:merchant_smith/part/arm_m
execute summon minecraft:item_display run function rpg:merchant_smith/part/body
execute summon minecraft:item_display run function rpg:merchant_smith/part/tunic
execute summon minecraft:item_display run function rpg:merchant_smith/part/leg_l
execute summon minecraft:item_display run function rpg:merchant_smith/part/leg_r
tag @s remove rpg.mer.model.dressing
function rpg:merchant_smith/anim/init
function rpg:merchant_smith/anim/enter/idle
