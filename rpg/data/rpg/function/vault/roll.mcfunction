# 抽一件放进自己（as 展示实体；#c = 场次，#mn = 2 时是灾厄最后一件）
tag @a remove rpg.vt.op
execute as @a if score @s rpg_vt_id = #c rpg_vt run tag @s add rpg.vt.op
scoreboard players add @a[tag=rpg.vt.op] rpg_vt_e 0
scoreboard players add @a[tag=rpg.vt.op] rpg_vt_l 0
scoreboard players set #e rpg_vt 0
scoreboard players set #l rpg_vt 0
execute as @a[tag=rpg.vt.op,limit=1] run scoreboard players operation #e rpg_vt = @s rpg_vt_e
execute as @a[tag=rpg.vt.op,limit=1] run scoreboard players operation #l rpg_vt = @s rpg_vt_l
execute store result score #r rpg_vt run random value 1..1000
scoreboard players set #q rpg_vt 1
execute unless score #mn rpg_vt matches 2 if score #r rpg_vt matches 1..8 run scoreboard players set #q rpg_vt 4
execute unless score #mn rpg_vt matches 2 if score #r rpg_vt matches 9..108 run scoreboard players set #q rpg_vt 3
execute unless score #mn rpg_vt matches 2 if score #r rpg_vt matches 109..438 run scoreboard players set #q rpg_vt 2
execute if score #mn rpg_vt matches 2 run scoreboard players set #q rpg_vt 2
execute if score #mn rpg_vt matches 2 if score #r rpg_vt matches 1..25 run scoreboard players set #q rpg_vt 4
execute if score #mn rpg_vt matches 2 if score #r rpg_vt matches 26..250 run scoreboard players set #q rpg_vt 3
execute if score #e rpg_vt matches 9.. if score #q rpg_vt matches ..1 run scoreboard players set #q rpg_vt 2
execute if score #l rpg_vt matches 39.. if score #q rpg_vt matches ..2 run scoreboard players set #q rpg_vt 3
scoreboard players set #mn rpg_vt 0
scoreboard players add @a[tag=rpg.vt.op] rpg_vt_n 1
scoreboard players add @a[tag=rpg.vt.op] rpg_vt_e 1
scoreboard players add @a[tag=rpg.vt.op] rpg_vt_l 1
scoreboard players add @a[tag=rpg.vt.op,scores={rpg_ps_21=2}] rpg_vt_e 1
scoreboard players add @a[tag=rpg.vt.op,scores={rpg_ps_21=2}] rpg_vt_l 1
execute if score #q rpg_vt matches 2.. run scoreboard players set @a[tag=rpg.vt.op] rpg_vt_e 0
execute if score #q rpg_vt matches 3.. run scoreboard players set @a[tag=rpg.vt.op] rpg_vt_l 0
scoreboard players operation @s rpg_vt_q = #q rpg_vt
execute if score #q rpg_vt matches 1 run loot replace entity @s contents loot rpg:vault/t1
execute if score #q rpg_vt matches 2 run loot replace entity @s contents loot rpg:vault/t2
execute if score #q rpg_vt matches 3 run loot replace entity @s contents loot rpg:vault/t3
execute if score #q rpg_vt matches 4 run loot replace entity @s contents loot rpg:vault/t4
execute if score #q rpg_vt matches 4 store result score #r rpg_vt run random value 1..20
execute if score #q rpg_vt matches 4 if score #r rpg_vt matches 1 run function rpg:vault/sakura
