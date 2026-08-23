# 图腾的一生：等圣水、点燃、按拍推进、收场。
# 由 rpg:exorcism 守卫调用 —— 场上没有图腾时整段跳过。
#
# 只有两条走查，都带类型。节拍不在这里展开：一支图腾一次调用，
# 剩下的分支全在 @s 上做 —— 那是自身作用域，不必再走一遍世界。

# 熄着的图腾等一朵圣水云。滞留药水落地留下的 area_effect_cloud 就是"浇上了"，
# 喷溅型落地即散，什么都留不下，所以驱魔圣水做成滞留型。
execute as @e[type=minecraft:item_display,tag=rpg.totem,tag=!rpg.totem.lit] at @s if entity @e[type=minecraft:area_effect_cloud,tag=rpg.holy_water,distance=..3] run function rpg:rite/light

# 点着的图腾走自己的节拍
execute as @e[type=minecraft:item_display,tag=rpg.totem.lit] at @s run function rpg:rite/beat
