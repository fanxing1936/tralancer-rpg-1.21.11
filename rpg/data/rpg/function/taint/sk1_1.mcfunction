# 携圣器亲历这一招，记下一份不可重复的罪证。
execute at @s as @a[tag=rpg.holy,distance=..18,gamemode=!spectator] run function rpg:inquest/clue/1_1
execute at @s as @a[distance=..14,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m1
# 原罪 —— 蛇矛沿视线破土，尖牙同路。
data modify storage rpg:demon uuid set from entity @s UUID
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..32] ~ ~ ~ 1 0.7
particle dust{color:[0.0,0.29,0.11],scale:2} ~ ~1 ~ 0.6 0.8 0.6 0.05 40
execute at @s anchored eyes facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run function rpg:taint/sk1_line with storage rpg:demon
