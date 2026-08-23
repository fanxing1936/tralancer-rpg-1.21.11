# 图腾的一生：等圣水、点燃、递减、炸开。
# 由 rpg:exorcism 守卫调用 —— 场上没有图腾时整段跳过。

# 熄着的图腾等一朵圣水云。滞留药水落地留下的 area_effect_cloud 就是"浇上了"，
# 喷溅型落地即散，什么都留不下，所以驱魔圣水做成滞留型。
execute as @e[type=minecraft:item_display,tag=rpg.totem,tag=!rpg.totem.lit] at @s if entity @e[type=minecraft:area_effect_cloud,distance=..3] run function rpg:rite/light

# 点着的图腾按拍净化，一拍比一拍弱
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=200}] at @s run function rpg:rite/p1
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=160}] at @s run function rpg:rite/p2
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=120}] at @s run function rpg:rite/p3
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=80}] at @s run function rpg:rite/p4
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=40}] at @s run function rpg:rite/p5

# 烧到头就炸
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=..0}] at @s run function rpg:rite/burst

execute as @e[tag=rpg.totem.lit] at @s run particle dust{color:[0.98,0.92,0.62],scale:1} ~ ~0.7 ~ 0.22 0.3 0.22 0.01 2
execute as @e[tag=rpg.totem.lit,scores={rpg_totem=1..}] run scoreboard players remove @s rpg_totem 1
