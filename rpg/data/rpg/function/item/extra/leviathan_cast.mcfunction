# 抛锚。`rotated ~ 0` 把俯仰归零，所以锚永远沿水平方向掷出 8 格，
# 不会因为抬头而飞上天 —— 锚是往下沉的东西。
# 血税。原本想直接改写 Health 来绕过无敌帧，但**玩家 NBT 是只读的** ——
# `execute store result entity @s Health` 对玩家不会生效（能解析，运行时静默失败），
# 所以那一版扣血根本没扣到。
#
# 改用 `damage`，伤害类型选 `minecraft:starve`：它是唯一同时位于
# `#bypasses_armor` 与 `#bypasses_effects` 的类型，所以护甲、保护附魔、
# 抗性提升一概不减免，每次实收 10 点。
# 它仍然要过约 10 刻的无敌帧 —— 但技能现在需要蓄力 30 刻，
# 两次施放之间必然超过无敌帧，这个顾虑随蓄力一起消失了。
# 生命已在 leviathan_fire 里确认高于 10，所以扣不死自己。
damage @s 10 minecraft:starve
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
scoreboard players reset @s rpg_levi_charge
