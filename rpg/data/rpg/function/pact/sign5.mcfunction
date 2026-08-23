# 第 5 柱 · 萨麦尔（暴怒）
scoreboard players set @s rpg_pact 5
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
attribute @s minecraft:attack_damage modifier remove rpg:pact/5/boon0
attribute @s minecraft:attack_damage modifier add rpg:pact/5/boon0 1.5 add_value
attribute @s minecraft:max_health modifier remove rpg:pact/5/bane0
attribute @s minecraft:max_health modifier add rpg:pact/5/bane0 -2 add_value
item replace entity @s weapon.mainhand with enchanted_book[custom_name=["",{"text":"[已立约]","italic":false,"color":"#7B241C","bold":true},{"text":"萨麦尔之柱","italic":false,"color":"white"}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"七十二柱之一，","italic":false,"color":"gray"},{"text":"所罗门","italic":false,"color":"#7B241C","bold":true},{"text":"封入柱中的名","italic":false,"color":"gray"}],["",{"text":"长按右键动用柱中之力（冷却 15 秒）","italic":false,"color":"gray"}],["",{"text":"在燃着的驱魔图腾旁长按则","italic":false,"color":"gray"},{"text":"毁约","italic":false,"color":"#FF3300","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"🜏恩赐","italic":false,"color":"white","bold":true},{"text":"　攻击伤害 +1.5，且攻击附带剧毒","italic":false,"color":"red"}],["",{"text":"🜏力量","italic":false,"color":"white","bold":true},{"text":"[毒雾]","italic":false,"color":"#7B241C","bold":true}],["",{"text":"　前方 7 格喷出毒雾，中者剧毒与凋零并存","italic":false,"color":"gray"}],["",{"text":"🜏枷锁","italic":false,"color":"white","bold":true},{"text":"　最大生命 −2","italic":false,"color":"dark_red"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"契约期间持续沾染","italic":false,"color":"gray"},{"text":"魔化","italic":false,"color":"dark_red","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_model_data={floats:[1110035.0f]},enchantment_glint_override=true,max_stack_size=1,food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100120f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]},custom_data={pact_tag:1b,pact:5,pact_signed:1b}]
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"#7B241C","bold":true}]
title @s subtitle ["",{"text":"萨麦尔之柱 · 暴怒","italic":false,"color":"red"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:8070172} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"#7B241C"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
