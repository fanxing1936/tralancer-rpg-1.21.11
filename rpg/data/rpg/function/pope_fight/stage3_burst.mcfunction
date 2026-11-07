execute as @e[type=minecraft:vindicator,tag=rpg.pf.boss] run function rpg:pope_fight/boss/remove
function rpg:pope_fight/fx/burst
# 旋风原声 13 秒，比动作长，到这里收掉。
stopsound @a[distance=..48] hostile rpg:pope.whirlwind
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.7
