# 血怒天罚 —— 死亡天使沿最近的血气突入人群。
execute at @s facing entity @a[limit=1,sort=nearest,gamemode=!spectator,gamemode=!creative] feet run tp @s ^ ^ ^5
particle flash{color:15158613} ~ ~1 ~ 0 0 0 0 1 normal
particle dust_color_transition{from_color:[0.89,0.30,0.30],to_color:[0.24,0.0,0.04],scale:3} ~ ~1 ~ 4 1.2 4 0.06 72 normal
particle sweep_attack ~ ~1 ~ 3 0.8 3 0 34 normal
particle trial_omen ~ ~1 ~ 4 1 4 0.1 72 normal
particle crit ~ ~1 ~ 4 1 4 0.22 72 normal
playsound minecraft:entity.ravager.roar hostile @a[distance=..36] ~ ~ ~ 1.2 0.8
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..40] ~ ~ ~ 0.8 1.15
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:taint/ult5_hit
