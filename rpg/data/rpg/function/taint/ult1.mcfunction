# 万蛇加冕 —— 三圈蛇牙从王冠下同时破土。
data modify storage rpg:demon uuid set from entity @s UUID
function rpg:taint/ult1_fangs with storage rpg:demon
particle dust_color_transition{from_color:[0.19,0.85,0.49],to_color:[0.0,0.18,0.07],scale:3} ~ ~1 ~ 5 1 5 0.04 72 normal
particle end_rod ~ ~2 ~ 2.5 1.5 2.5 0.05 72 normal
particle flash{color:3266940} ~ ~2 ~ 0 0 0 0 1 normal
particle dragon_breath ~ ~1 ~ 4 1 4 0.08 72 normal
particle enchanted_hit ~ ~1 ~ 4 1 4 0.12 72 normal
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..32] ~ ~ ~ 1.2 0.55
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 0.7
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult1_hit
