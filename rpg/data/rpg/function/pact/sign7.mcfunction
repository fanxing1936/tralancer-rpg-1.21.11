# 第 7 柱 · 玛门（贪婪）
scoreboard players set @s rpg_pact 7
scoreboard players set @s rpg_pact_cd 300
tag @s add rpg.pact
# 这一柱不靠属性修饰符 —— 它的恩赐与枷锁都是逐刻的
item replace entity @s weapon.mainhand with enchanted_book[custom_name=["",{"text":"[已立约]","italic":false,"color":"#B7950B","bold":true},{"text":"玛门之柱","italic":false,"color":"#FFFFFF","bold":false}],lore=[["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"七十二柱之一，","italic":false,"color":"gray"},{"text":"所罗门","italic":false,"color":"#B7950B","bold":true},{"text":"封入柱中的名","italic":false,"color":"gray"}],["",{"text":"长按右键动用柱中之力（冷却 15 秒）","italic":false,"color":"gray"}],["",{"text":"在燃着的驱魔图腾旁长按则","italic":false,"color":"gray"},{"text":"毁约","italic":false,"color":"#FF3300","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"🜏恩赐","italic":false,"color":"white","bold":true},{"text":"　6 格内的掉落物自动吸附到身边","italic":false,"color":"gold"}],["",{"text":"🜏力量","italic":false,"color":"white","bold":true},{"text":"[点金]","italic":false,"color":"#B7950B","bold":true}],["",{"text":"　8 格内的掉落物尽数翻倍，并吐出经验","italic":false,"color":"gray"}],["",{"text":"🜏枷锁","italic":false,"color":"white","bold":true},{"text":"　魔化沾染速度翻倍","italic":false,"color":"dark_red"}],["",{"text":"+------------------+","italic":false,"color":"white"}],["",{"text":"契约期间持续沾染","italic":false,"color":"gray"},{"text":"魔化","italic":false,"color":"dark_red","bold":true}],["",{"text":"+------------------+","italic":false,"color":"white"}]],custom_model_data={floats:[1110037.0f]},enchantment_glint_override=true,max_stack_size=1,food={nutrition:0,saturation:0f,can_always_eat:1b},consumable={consume_seconds:100120f,animation:"block",sound:"minecraft:block.enchantment_table.use",has_consume_particles:false,on_consume_effects:[]},custom_data={pact_tag:1b,pact:7,pact_signed:1b}]
title @s times 10 70 20
title @s title ["",{"text":"契 约 已 立","italic":false,"color":"#B7950B","bold":true}]
title @s subtitle ["",{"text":"玛门之柱 · 贪婪","italic":false,"color":"#B7950B"}]
playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.8 0.6
playsound minecraft:entity.wither.spawn master @a[distance=..32] ~ ~ ~ 0.5 1.4
execute at @s run particle sculk_charge_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 60
execute at @s run particle minecraft:flash{color:12031243} ~ ~1 ~ 0 0 0 0 1
tellraw @s ["",{"text":"◆ ","color":"#B7950B"},{"text":"魔神借契约进入你的心。","color":"gray","italic":true}]
