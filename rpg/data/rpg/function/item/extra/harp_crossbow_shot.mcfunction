# 竖琴弩［齐奏］—— 由 rpg:advancement/item/harp_crossbow 在射击时触发。
# 多重射击已经射出三支（±10°），这里再向两侧各补一支。
advancement revoke @s only rpg:item/harp_crossbow
tag @s add rpg.hc.cast
execute anchored eyes positioned ^ ^ ^ rotated ~-22 ~ run function rpg:item/extra/harp_crossbow_bolt
execute anchored eyes positioned ^ ^ ^ rotated ~22 ~ run function rpg:item/extra/harp_crossbow_bolt
playsound minecraft:block.note_block.harp player @a[distance=..16] ~ ~ ~ 0.8 1.4
execute anchored eyes positioned ^ ^ ^1 run particle minecraft:note ~ ~0.2 ~ 0.4 0.2 0.4 1 3
tag @s remove rpg.hc.cast
