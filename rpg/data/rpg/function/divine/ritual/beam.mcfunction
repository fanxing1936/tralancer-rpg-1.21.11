# 绑定阶段的神圣伤害转化为法阵稳定度，不再被 420 HP 回填吞没。
tag @s add rpg.divine.ritual_subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.divine.ritual_subject,limit=1,sort=nearest] rpg_rite_id run function rpg:divine/ritual/beam_apply
tag @s remove rpg.divine.ritual_subject
particle minecraft:flash{color:8641023} ~ ~1 ~ 0 0 0 0 1 force
