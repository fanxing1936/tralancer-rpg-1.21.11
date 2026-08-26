title @a[distance=..24,gamemode=!spectator] times 0 22 4
title @a[distance=..24,gamemode=!spectator] subtitle ["",{"text":"贝利尔 · 罪域聚能","color":"#5B2C6F","italic":false,"bold":false},{"text":" · 退入法阵四格庇护圈","color":"#FFF2A8","italic":false}]
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:1.4} ~ ~0.25 ~ 5 0.08 5 0.018 52 force
particle dust_color_transition{from_color:[0.75,0.42,0.91],to_color:[0.12,0.0,0.18],scale:2.1} ~ ~0.35 ~ 10 0.12 10 0.035 82 force
particle reverse_portal ~ ~1.0 ~ 7 0.8 7 0.035 36 force
particle trial_spawner_detection_ominous ~ ~0.2 ~ 11 0.05 11 0.012 48 force
playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.58
