# 波阿斯［承力］与双生联动［圣殿］
# 圣殿：任意一手雅斤 + 另一手波阿斯即成立
tag @a remove rpg.twin
tag @a[tag=rpg.h.jachin_tag1,tag=rpg.o.boaz_tag1] add rpg.twin
tag @a[tag=rpg.h.boaz_tag1,tag=rpg.o.jachin_tag1] add rpg.twin

# 承力：本次是否有命中（主手或副手握着波阿斯都算）
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={boaz=0..},tag=rpg.h.boaz_tag1] run tag @s add rpg.boaz.src
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={boaz=0..},tag=rpg.o.boaz_tag1] run tag @s add rpg.boaz.src
execute as @a[tag=rpg.boaz.src] run scoreboard players add @s rpg_boaz_stack 1
execute as @a[tag=rpg.boaz.src,tag=!rpg.twin,scores={rpg_boaz_stack=3..}] run tag @s add rpg.boaz.burst
execute as @a[tag=rpg.boaz.src,tag=rpg.twin,scores={rpg_boaz_stack=2..}] run tag @s add rpg.boaz.burst
execute as @a[tag=rpg.boaz.burst] run scoreboard players set @s rpg_boaz_stack 0
execute as @a[tag=rpg.boaz.burst] at @s run playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..14]

# 强化打击落在刚被打中的目标上
execute if entity @e[tag=rpg.hurt] run function rpg:item/extra/twin/g0
execute as @e[tag=rpg.hurt,type=!player] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run damage @s 6 minecraft:player_attack by @a[tag=rpg.boaz.burst,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,type=!player] at @s if entity @a[tag=rpg.boaz.burst,distance=..7] run effect give @s minecraft:weakness 4 1 true

# 圣殿：两把剑各掠一道，紫金与青粉同时闪过
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.twin,distance=..7] run particle dust_color_transition{from_color:[0.478,0.086,0.584],to_color:[0.949,0.851,0.404],scale:2} ~ ~1 ~ 0.45 0.5 0.45 0.06 22
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.twin,distance=..7] run particle dust_color_transition{from_color:[0.078,0.510,0.569],to_color:[0.871,0.561,0.949],scale:2} ~ ~1.2 ~ 0.45 0.5 0.45 0.06 22

tag @a[tag=rpg.boaz.src] remove rpg.boaz.src
tag @a[tag=rpg.boaz.burst] remove rpg.boaz.burst
scoreboard players reset * boaz
