# 紫宴朝圣 —— 意志被拖向宴席中央，再献出自己的血。
particle portal ~ ~1 ~ 5 1.5 5 0.65 72 normal
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:3} ~ ~1 ~ 4 1 4 0.06 72 normal
particle flash{color:12610536} ~ ~1 ~ 0 0 0 0 1 normal
particle witch ~ ~1 ~ 5 1.5 5 0.18 72 normal
particle reverse_portal ~ ~1 ~ 4 1 4 0.28 72 normal
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..36] ~ ~ ~ 1.2 0.5
playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..36] ~ ~ ~ 1.1 0.55
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult6_hit
