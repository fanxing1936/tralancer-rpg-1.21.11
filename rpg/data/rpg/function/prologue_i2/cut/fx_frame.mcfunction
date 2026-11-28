scoreboard players set #fxc rpg_pr_i2 0
# 裂缝：张开时 0→7，之后在 4～7 之间循环；合上时倒放，放完就撤
execute if score #rift rpg_pr_i2 matches 1 run scoreboard players add #rf rpg_pr_i2 1
execute if score #rift rpg_pr_i2 matches 1 if score #rf rpg_pr_i2 matches 8.. run scoreboard players set #rf rpg_pr_i2 4
execute if score #rift rpg_pr_i2 matches 2 run scoreboard players remove #rf rpg_pr_i2 1
execute if score #rift rpg_pr_i2 matches 0 run scoreboard players set #rf rpg_pr_i2 -1
execute if score #rf rpg_pr_i2 matches ..-1 run kill @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..]
execute if score #rf rpg_pr_i2 matches ..-1 if score #rift rpg_pr_i2 matches 2 run scoreboard players set #rift rpg_pr_i2 0
execute if score #rf rpg_pr_i2 matches ..-1 run scoreboard players set #rf rpg_pr_i2 0
execute if score #rf rpg_pr_i2 matches 0 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_0"
execute if score #rf rpg_pr_i2 matches 1 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_1"
execute if score #rf rpg_pr_i2 matches 2 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_2"
execute if score #rf rpg_pr_i2 matches 3 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_3"
execute if score #rf rpg_pr_i2 matches 4 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_4"
execute if score #rf rpg_pr_i2 matches 5 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_5"
execute if score #rf rpg_pr_i2 matches 6 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_6"
execute if score #rf rpg_pr_i2 matches 7 as @e[type=minecraft:item_display,tag=rpg.pr.riftv,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/rift_7"
scoreboard players add #sf rpg_pr_i2 1
execute if score #sf rpg_pr_i2 matches 8.. run scoreboard players set #sf rpg_pr_i2 0
execute if score #sf rpg_pr_i2 matches 0 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_0"
execute if score #sf rpg_pr_i2 matches 1 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_1"
execute if score #sf rpg_pr_i2 matches 2 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_2"
execute if score #sf rpg_pr_i2 matches 3 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_3"
execute if score #sf rpg_pr_i2 matches 4 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_4"
execute if score #sf rpg_pr_i2 matches 5 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_5"
execute if score #sf rpg_pr_i2 matches 6 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_6"
execute if score #sf rpg_pr_i2 matches 7 as @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_7"
execute if score #sf rpg_pr_i2 matches 0 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_0"
execute if score #sf rpg_pr_i2 matches 1 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_1"
execute if score #sf rpg_pr_i2 matches 2 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_2"
execute if score #sf rpg_pr_i2 matches 3 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_3"
execute if score #sf rpg_pr_i2 matches 4 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_4"
execute if score #sf rpg_pr_i2 matches 5 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_5"
execute if score #sf rpg_pr_i2 matches 6 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_6"
execute if score #sf rpg_pr_i2 matches 7 as @e[type=minecraft:item_display,tag=rpg.pr.wisp,distance=0..] run data modify entity @s item.components."minecraft:item_model" set value "rpg:prologue_fx/smoke_7"
