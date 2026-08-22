# 震荡只波及命中目标周围 3 格，不做全场扫描。
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run damage @s 3 minecraft:magic by @a[tag=rpg.epic.chime,limit=1,sort=nearest]
execute as @e[distance=0.1..3,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run particle dust_color_transition{from_color:11121336,to_color:5004652,scale:1} ~ ~1 ~ 0.25 0.4 0.25 0.04 10
