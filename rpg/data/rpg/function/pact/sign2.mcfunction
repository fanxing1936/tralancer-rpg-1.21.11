# 第 2 柱 · 利维坦（嫉妒）
scoreboard players set @s rpg_pact 2
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
attribute @s minecraft:movement_speed modifier remove rpg:pact/2/boon0
attribute @s minecraft:movement_speed modifier add rpg:pact/2/boon0 0.008 add_value
attribute @s minecraft:max_health modifier remove rpg:pact/2/bane0
attribute @s minecraft:max_health modifier add rpg:pact/2/bane0 -4 add_value
item replace entity @s weapon.mainhand with enchanted_book[custom_name=["",{"text":"[已立约]","italic":false,"color":"#1B4F72","bold":true},{"text":"利维坦之柱","italic":false,"color":"#FFFFFF","bold":false}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"七十二柱之一，","italic":false,"color":"gray"},{"text":"所罗门","italic":false,"color":"#1B4F72","bold":true},{"text":"封入柱中的名","italic":false,"color":"gray"}],["",{"text":"长按右键动用柱中之力（冷却 15 秒）","italic":false,"color":"gray"}],["",{"text":"在燃着的驱魔图腾旁长按则","italic":false,"color":"gray"},{"text":"毁约","italic":false,"color":"#FF3300","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"🜏恩赐","italic":false,"color":"white","bold":true},{"text":"　移动速度 +8%","italic":false,"color":"aqua"}],["",{"text":"🜏力量","italic":false,"color":"white","bold":true},{"text":"[沉锚]","italic":false,"color":"#1B4F72","bold":true}],["",{"text":"　向前方抛出巨锚，锚落处涌起漩涡，将敌人拖向锚心并持续碾压","italic":false,"color":"gray"}],["",{"text":"🜏枷锁","italic":false,"color":"white","bold":true},{"text":"　最大生命 −4","italic":false,"color":"dark_red"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"契约期间持续沾染","italic":false,"color":"gray"},{"text":"魔化","italic":false,"color":"dark_red","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_model_data={floats:[1110032.0f]},enchantment_glint_override=true,max_stack_size=1,food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100120f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]},custom_data={pact_tag:1b,pact:2,pact_signed:1b}]
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"#1B4F72","bold":true}]
title @s subtitle ["",{"text":"利维坦之柱 · 嫉妒","italic":false,"color":"#1B4F72"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:1789810} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"#1B4F72"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
