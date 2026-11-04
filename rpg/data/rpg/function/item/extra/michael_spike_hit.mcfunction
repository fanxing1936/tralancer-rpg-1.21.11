# 被骨刺挑中的一个。恶魔伤害提高一半并被点燃。
tag @s remove rpg.mi.spiked
execute if entity @s[tag=rpg.demon] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.demon.minion] run tag @s add rpg.mi.foe
execute if entity @s[tag=!rpg.mi.foe] run damage @s 8 minecraft:magic by @a[tag=rpg.mi.cast,limit=1]
execute if entity @s[tag=rpg.mi.foe] run damage @s 12 minecraft:magic by @a[tag=rpg.mi.cast,limit=1]
execute if entity @s[tag=rpg.mi.foe] run data modify entity @s Fire set value 80s
data modify entity @s Motion[1] set value 0.55d
particle block{block_state:{Name:"minecraft:bone_block"}} ~ ~0.8 ~ 0.3 0.4 0.3 0 8
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.4} ~ ~1 ~ 0.3 0.4 0.3 0.02 8
# 骨中之骨：骨刺挑中的直接叠上一层圣焰
execute if entity @a[tag=rpg.mi.cast,tag=rpg.mi.pair] run tag @a[tag=rpg.mi.cast] add rpg.mi.owner
execute if entity @a[tag=rpg.mi.owner] run function rpg:item/extra/michael_mark
tag @a[tag=rpg.mi.owner] remove rpg.mi.owner
tag @s remove rpg.mi.foe
