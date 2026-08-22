# 抛锚。`rotated ~ 0` 把俯仰归零，所以锚永远沿水平方向掷出 8 格，
# 不会因为抬头而飞上天 —— 锚是往下沉的东西。
xp add @s -2 levels
tag @s add rpg.levi.cast
# 凌空抛锚沉得更深：脚下悬空就是"从高处砸下"，与重锤的本能一致
execute at @s if block ~ ~-1 ~ air run tag @s add rpg.levi.airborne
particle dust_color_transition{from_color:16559622,to_color:1195644,scale:1} ~ ~1.1 ~ 0.3 0.4 0.3 0.02 16
playsound minecraft:block.chain.break player @a[distance=..24] ~ ~ ~ 1 0.6
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.7
execute at @s rotated ~ 0 positioned ^ ^ ^8 run function rpg:item/extra/leviathan_drop
tag @s remove rpg.levi.airborne
tag @s remove rpg.levi.cast
