
# 兼容清理旧版已生成、没有主人可追溯的樱花箭；新版不再生成它们。
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s run particle dust_color_transition{from_color:[0.4,0.0,1.0],to_color:[0.0,0.0,0.0],scale:1} ~ ~ ~ 0.3 0.3 0.3 0.1 8
kill @e[type=minecraft:spectral_arrow,tag=sakura_tag]
