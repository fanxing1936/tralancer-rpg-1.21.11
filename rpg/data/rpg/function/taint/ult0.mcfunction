# 无名蚀界 —— 无名者没有柱位，只把周围的一切称谓抹黑。
particle squid_ink ~ ~1 ~ 5 1.5 5 0.18 72 normal
particle sculk_soul ~ ~1 ~ 4 1 4 0.09 72 normal
particle dust_color_transition{from_color:[0.82,0.23,0.28],to_color:[0.0,0.0,0.0],scale:3} ~ ~1 ~ 4 1 4 0.05 72 normal
particle flash{color:13777735} ~ ~1 ~ 0 0 0 0 1 normal
particle trial_omen ~ ~1 ~ 4 1 4 0.1 72 normal
particle reverse_portal ~ ~1 ~ 4 1.5 4 0.3 72 normal
playsound minecraft:entity.warden.roar hostile @a[distance=..36] ~ ~ ~ 1.1 0.55
playsound minecraft:entity.wither.spawn hostile @a[distance=..40] ~ ~ ~ 0.7 0.45
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult0_hit
