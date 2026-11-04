# 谁似神：天使长的呼喊。前方 10 格骨刺破土，双持骨中之骨时延到 16 格。
scoreboard players operation @s rpg_mi_cd = #now rpg_mi_tmp
scoreboard players add @s rpg_mi_cd 160
tag @s add rpg.mi.cast
particle flash{color:16724736} ~ ~0.2 ~ 0 0 0 0 1
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.4} ~ ~0.4 ~ 0.6 0.2 0.6 0.02 20
playsound minecraft:block.bone_block.break player @a[distance=..24] ~ ~ ~ 1 0.5
playsound minecraft:entity.blaze.shoot player @a[distance=..24] ~ ~ ~ 0.8 0.6
playsound minecraft:item.totem.use player @a[distance=..24] ~ ~ ~ 0.35 1.8

execute rotated ~ 0 run function rpg:item/extra/michael_spikes
execute if entity @s[tag=rpg.mi.pair] rotated ~ 0 run function rpg:item/extra/michael_spikes_far
execute as @e[tag=rpg.mi.spiked] at @s run function rpg:item/extra/michael_spike_hit

tag @s remove rpg.mi.cast
# 骨刺自己的伤害不算肋骨命中：清掉这一刻记下的输出
scoreboard players reset @s rpg_mi_dmg
