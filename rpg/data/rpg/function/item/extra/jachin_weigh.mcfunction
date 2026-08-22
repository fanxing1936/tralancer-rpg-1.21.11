# 天平在目标头顶张开，然后落下判决。
# 生命值还厚的，削去"亏欠"；已经残破的，直接显出亏欠 —— 重创。
particle dust_color_transition{from_color:[0.478,0.086,0.584],to_color:[0.949,0.851,0.404],scale:1} ~ ~1.3 ~ 0.28 0.45 0.28 0.02 16
particle end_rod ~ ~1.7 ~ 0.32 0.12 0.32 0.01 6
particle minecraft:flash{color:15915367} ~ ~1.5 ~ 0 0 0 0 1
effect give @s minecraft:glowing 5 0 true

execute unless entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={damage_action=20..}] run damage @s 8 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute unless entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={damage_action=..19}] run damage @s 14 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute if entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={damage_action=30..}] run damage @s 12 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]
execute if entity @a[tag=rpg.jachin.temple,distance=..16] if entity @s[scores={damage_action=..29}] run damage @s 20 minecraft:magic by @a[tag=rpg.jachin.cast,limit=1,sort=nearest]

# 显出亏欠的那一下额外给个紫色爆闪与判决音
execute if entity @s[scores={damage_action=..19}] run particle minecraft:flash{color:8001173} ~ ~1.1 ~ 0 0 0 0 1
execute if entity @s[scores={damage_action=..19}] run particle dust_color_transition{from_color:[0.949,0.851,0.404],to_color:[0.478,0.086,0.584],scale:2} ~ ~1 ~ 0.4 0.5 0.4 0.06 30
execute if entity @s[scores={damage_action=..19}] run playsound minecraft:entity.evoker.cast_spell player @a[distance=..16] ~ ~ ~ 1 0.8
