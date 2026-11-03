# 万蝇饕宴 —— 灰烬遮天，饥群从宴席中孵化。
particle ash ~ ~1 ~ 5 2 5 0.15 72 normal
particle mycelium ~ ~1 ~ 4 1.5 4 0.18 72 normal
particle dust_color_transition{from_color:[0.71,0.85,0.34],to_color:[0.35,0.42,0.12],scale:2.6} ~ ~1 ~ 4 1 4 0.05 72 normal
particle flash{color:12044363} ~ ~1 ~ 0 0 0 0 1 normal
particle large_smoke ~ ~1 ~ 5 1.5 5 0.14 72 normal
particle spore_blossom_air ~ ~2 ~ 5 2 5 0.08 72 normal
playsound minecraft:entity.bee.loop_aggressive hostile @a[distance=..36] ~ ~ ~ 1.25 0.45
playsound minecraft:entity.ravager.roar hostile @a[distance=..40] ~ ~ ~ 0.65 0.55
function rpg:taint/ult4_swarm
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult4_hit
# 别西卜外观（add_beelzebub.py）
execute if entity @s[tag=rpg.bz] run function rpg:beelzebub/skill/ult4
