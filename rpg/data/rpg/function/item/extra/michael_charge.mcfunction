# 蓄势：脊髓里的圣火往上涌
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.4} ~ ~1 ~ 0.35 0.45 0.35 0 2
execute if score @s rpg_mi_hold matches 1 run playsound minecraft:block.bone_block.place player @a[distance=..16] ~ ~ ~ 0.8 0.6
execute if score @s rpg_mi_hold matches 10 run playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 0.6 1.6
