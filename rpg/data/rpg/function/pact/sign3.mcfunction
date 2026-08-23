# 第 3 柱 · 亚巴顿（怠惰）
scoreboard players set @s rpg_pact 3
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
attribute @s minecraft:max_health modifier remove rpg:pact/3/boon0
attribute @s minecraft:max_health modifier add rpg:pact/3/boon0 6 add_value
attribute @s minecraft:movement_speed modifier remove rpg:pact/3/bane0
attribute @s minecraft:movement_speed modifier add rpg:pact/3/bane0 -0.012 add_value
item replace entity @s weapon.mainhand with enchanted_book[custom_name=["",{"text":"[已立约]","italic":false,"color":"#6A6A70","bold":true},{"text":"亚巴顿之柱","italic":false,"color":"white"}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"七十二柱之一，","italic":false,"color":"gray"},{"text":"所罗门","italic":false,"color":"#6A6A70","bold":true},{"text":"封入柱中的名","italic":false,"color":"gray"}],["",{"text":"长按右键动用柱中之力（冷却 15 秒）","italic":false,"color":"gray"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"🜏恩赐","italic":false,"color":"white","bold":true},{"text":"　最大生命 +6","italic":false,"color":"gray"}],["",{"text":"🜏力量","italic":false,"color":"white","bold":true},{"text":"[收割]","italic":false,"color":"#6A6A70","bold":true}],["",{"text":"　周身 6 格爆发灵魂收割，每收割一个目标回复 1 颗心","italic":false,"color":"gray"}],["",{"text":"🜏枷锁","italic":false,"color":"white","bold":true},{"text":"　移动速度 −12%","italic":false,"color":"dark_red"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"契约期间持续沾染","italic":false,"color":"gray"},{"text":"魔化","italic":false,"color":"dark_red","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_model_data={floats:[1110033.0f]},enchantment_glint_override=true,max_stack_size=1,food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100120f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]},custom_data={pact_tag:1b,pact:3,pact_signed:1b}]
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"#6A6A70","bold":true}]
title @s subtitle ["",{"text":"亚巴顿之柱 · 怠惰","italic":false,"color":"gray"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:6974064} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"#6A6A70"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
