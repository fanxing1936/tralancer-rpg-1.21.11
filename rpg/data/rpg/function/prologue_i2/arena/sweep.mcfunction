# 每秒一次：清掉场地上弹出来的红石粉（群系血迹是红石线，压平地面、踩碎石台时会掉）
scoreboard players set #sweep rpg_pr_i2 0
# 顺带每秒补一次饱和（死亡重生等会清掉效果）
effect give @a[tag=rpg.pri2] minecraft:saturation infinite 0 true
execute in rpg:armageddon_2 positioned 0 60 0 as @e[type=minecraft:item,distance=..72] if items entity @s contents minecraft:redstone run kill @s
