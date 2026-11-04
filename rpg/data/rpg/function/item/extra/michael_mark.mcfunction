# 叠一层圣焰。施加者带 rpg.mi.owner；它若双持骨中之骨，第二层就引燃。
execute if entity @s[tag=rpg.mi.fuse] run return 0
# 有圣焰在烧，守卫就得继续放行 —— 施加者换下圣骸，引信和余烬也照常走完
scoreboard players set #mi_live rpg_mi_tmp 1
scoreboard players add @s rpg_mi_flame 1
scoreboard players set @s rpg_mi_ttl 100
tag @s add rpg.mi.marked
scoreboard players set #need rpg_mi_tmp 3
execute if entity @a[tag=rpg.mi.owner,tag=rpg.mi.pair] run scoreboard players set #need rpg_mi_tmp 2
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.4} ~ ~1.1 ~ 0.25 0.35 0.25 0.02 6
execute if score @s rpg_mi_flame >= #need rpg_mi_tmp run function rpg:item/extra/michael_kindle
