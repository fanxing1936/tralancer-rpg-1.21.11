# prologue_multi hub
# 管理员：中止所有战场，所有人还原，排队清空
execute in rpg:armageddon as @a[tag=rpg.pri1] run function rpg:prologue_i1/iso/restore
execute in rpg:armageddon run function rpg:prologue_i1/cleanup
scoreboard players set #owe rpg_pr_i1 0
execute in rpg:armageddon_2 as @a[tag=rpg.pri2] run function rpg:prologue_i2/iso/restore
execute in rpg:armageddon_2 run function rpg:prologue_i2/cleanup
scoreboard players set #owe rpg_pr_i2 0
execute in rpg:armageddon_3 as @a[tag=rpg.pri3] run function rpg:prologue_i3/iso/restore
execute in rpg:armageddon_3 run function rpg:prologue_i3/cleanup
scoreboard players set #owe rpg_pr_i3 0
execute in rpg:armageddon_4 as @a[tag=rpg.pri4] run function rpg:prologue_i4/iso/restore
execute in rpg:armageddon_4 run function rpg:prologue_i4/cleanup
scoreboard players set #owe rpg_pr_i4 0
tag @a remove rpg.pr.q
tag @a remove rpg.pr.pick
scoreboard players reset @a rpg_pr_g
tellraw @s {"text":"[序章] 所有战场已中止。","color":"#E8D9B0"}
