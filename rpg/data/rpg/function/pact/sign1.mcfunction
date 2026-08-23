# 第 1 柱 · 路西法（傲慢）
scoreboard players set @s rpg_pact 1
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
attribute @s minecraft:attack_damage modifier remove rpg:pact/1/boon0
attribute @s minecraft:attack_damage modifier add rpg:pact/1/boon0 2.5 add_value
attribute @s minecraft:knockback_resistance modifier remove rpg:pact/1/bane0
attribute @s minecraft:knockback_resistance modifier add rpg:pact/1/bane0 -0.25 add_value
item replace entity @s weapon.mainhand with enchanted_book[custom_name=["",{"text":"[已立约]","italic":false,"color":"#00491c","bold":true},{"text":"路西法之柱","italic":false,"color":"white"}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"七十二柱之一，","italic":false,"color":"gray"},{"text":"所罗门","italic":false,"color":"#00491c","bold":true},{"text":"封入柱中的名","italic":false,"color":"gray"}],["",{"text":"长按右键动用柱中之力（冷却 15 秒）","italic":false,"color":"gray"}],["",{"text":"在燃着的驱魔图腾旁长按则","italic":false,"color":"gray"},{"text":"毁约","italic":false,"color":"#FF3300","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"🜏恩赐","italic":false,"color":"white","bold":true},{"text":"　攻击伤害 +2.5","italic":false,"color":"green"}],["",{"text":"🜏力量","italic":false,"color":"white","bold":true},{"text":"[原罪]","italic":false,"color":"#00491c","bold":true}],["",{"text":"　沿视线刺出蛇矛，幻魔者尖牙同路破土；贯穿者受伤加重并向近旁蔓延","italic":false,"color":"gray"}],["",{"text":"🜏枷锁","italic":false,"color":"white","bold":true},{"text":"　击退抗性 −0.25（更容易被打飞）","italic":false,"color":"dark_red"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"契约期间持续沾染","italic":false,"color":"gray"},{"text":"魔化","italic":false,"color":"dark_red","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_model_data={floats:[1110031.0f]},enchantment_glint_override=true,max_stack_size=1,food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100120f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]},custom_data={pact_tag:1b,pact:1,pact_signed:1b}]
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"#00491c","bold":true}]
title @s subtitle ["",{"text":"路西法之柱 · 傲慢","italic":false,"color":"green"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:18716} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"#00491c"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
