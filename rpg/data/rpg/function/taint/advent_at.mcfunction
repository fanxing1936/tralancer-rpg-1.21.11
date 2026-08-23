particle explosion ~ ~1 ~ 0 0 0 0 1
particle sculk_soul ~ ~1 ~ 0.6 1 0.6 0.08 80
particle dust{color:[0.35,0.0,0.05],scale:3} ~ ~1 ~ 0.8 1.2 0.8 0.05 90
particle explosion_emitter ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.wither.spawn hostile @a[distance=..48] ~ ~ ~ 1 0.6
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1 0.5
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 0.8 0.7

# 这一行由 add_pact 改写成七柱分流 —— 那边才认识柱位。
function rpg:taint/lord
