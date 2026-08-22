# 抛锚。`rotated ~ 0` 把俯仰归零，所以锚永远沿水平方向掷出 8 格，
# 不会因为抬头而飞上天 —— 锚是往下沉的东西。
# 血税：直接改写生命值，而不是 `damage`。
# `damage` 要过约 10 刻的无敌帧 —— 连点右键时代价会被整个吞掉，等于白嫖；
# 直接写 Health 则绕过护甲、抗性与无敌帧，每一次都实收 10 点。
# 命中前已经在 trigger 里确认过生命高于 10，所以不会把自己写死。
scoreboard players remove @s rpg_levi_hp 10
execute store result entity @s Health float 1 run scoreboard players get @s rpg_levi_hp
effect give @s minecraft:unluck 10 0 true
particle damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 12
playsound minecraft:entity.player.hurt_drown player @s ~ ~ ~ 1 0.7
tag @s add rpg.levi.cast
# 凌空抛锚沉得更深：脚下悬空就是"从高处砸下"，与重锤的本能一致
execute at @s if block ~ ~-1 ~ air run tag @s add rpg.levi.airborne
particle dust_color_transition{from_color:16559622,to_color:1195644,scale:1} ~ ~1.1 ~ 0.3 0.4 0.3 0.02 16
playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.7
execute at @s rotated ~ 0 positioned ^ ^ ^8 run function rpg:item/extra/leviathan_drop
tag @s remove rpg.levi.airborne
tag @s remove rpg.levi.cast
