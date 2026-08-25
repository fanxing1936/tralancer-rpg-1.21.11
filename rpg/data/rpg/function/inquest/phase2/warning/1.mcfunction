title @a[distance=..24,gamemode=!spectator] times 0 22 4
title @a[distance=..24,gamemode=!spectator] subtitle ["",{"text":"路西法 · 罪域聚能","color":"#00491C","italic":false,"bold":true},{"text":" · 退入法阵四格庇护圈","color":"#FFF2A8","italic":false}]
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:1.4} ~ ~0.25 ~ 5 0.08 5 0.018 52 force
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:2.1} ~ ~0.35 ~ 10 0.12 10 0.035 82 force
particle end_rod ~ ~1.0 ~ 7 0.8 7 0.035 36 force
particle trial_spawner_detection_ominous ~ ~0.2 ~ 11 0.05 11 0.012 48 force
playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 0.9 0.58
