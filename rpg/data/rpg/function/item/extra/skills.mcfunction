# 新锻装备的原创技能总入口。由 rpg:command/tick 每刻调用一次。
#
# 每条都先过一次守卫：没人拿着这件武器、场上也没有它留下的痕迹时，
# 整个函数直接跳过。空闲一刻的代价因此只是几次标签检查，而不是十几次全场遍历。
# 箭矢类的技能要在射手换手之后仍然把箭送完，所以第二个条件看的是箭上的标记；
# 藤蔓之鞭同理，连击一旦起手就要抽满六鞭。
execute if entity @a[tag=rpg.h.deep_seek_tag1] run function rpg:item/extra/deep_seek
execute unless entity @a[tag=rpg.h.deep_seek_tag1] if entity @e[tag=rpg.deep] run function rpg:item/extra/deep_seek
execute if entity @a[tag=rpg.h.mischief_tag1] run function rpg:item/extra/mischief
execute unless entity @a[tag=rpg.h.mischief_tag1] if entity @e[tag=rpg.mis] run function rpg:item/extra/mischief
execute if entity @a[tag=rpg.h.rift_tag1] run function rpg:item/extra/rift
execute unless entity @a[tag=rpg.h.rift_tag1] if entity @e[tag=rpg.rift] run function rpg:item/extra/rift
execute if entity @a[tag=rpg.h.vine_tag1] run function rpg:item/extra/vine
execute unless entity @a[tag=rpg.h.vine_tag1] if entity @e[tag=rpg.vine.lash] run function rpg:item/extra/vine
execute if entity @a[tag=rpg.h.truth_tag1] run function rpg:item/extra/truth
execute if entity @a[tag=rpg.h.boaz_tag1] run function rpg:item/extra/twin
execute unless entity @a[tag=rpg.h.boaz_tag1] if entity @a[tag=rpg.o.boaz_tag1] run function rpg:item/extra/twin
execute if entity @a[tag=rpg.h.lucifer_tag1] run function rpg:item/extra/lucifer
execute unless entity @a[tag=rpg.h.lucifer_tag1] if entity @e[tag=rpg.luci.sin] run function rpg:item/extra/lucifer
execute if entity @a[tag=rpg.h.leviathan_tag1] run function rpg:item/extra/leviathan
execute unless entity @a[tag=rpg.h.leviathan_tag1] if entity @e[tag=rpg.levi.anchor] run function rpg:item/extra/leviathan
