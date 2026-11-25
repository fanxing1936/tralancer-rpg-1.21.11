scoreboard players operation @s rpg_vt_id = #id rpg_vt
scoreboard players set @s rpg_vt_t 0
scoreboard players set @s rpg_vt_m 1
data modify entity @s data.owner set from entity @a[tag=rpg.vt.op,limit=1] UUID
execute facing entity @p[tag=rpg.vt.op] feet run rotate @s ~ 0
tag @s remove rpg.vt.new
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_0
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_1
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_2
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_3
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_4
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_5
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_6
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_7
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_8
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.vt.i","rpg.vt.new"],item_display:"fixed",teleport_duration:1,view_range:0.6f,brightness:{block:15,sky:15},transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.010f,0.010f,0.010f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s as @e[type=minecraft:item_display,tag=rpg.vt.new,distance=..2,limit=1] run function rpg:vault/slot_1_9
playsound minecraft:block.vault.open_shutter block @a[distance=..20] ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.activate block @a[distance=..20] ~ ~ ~ 0.7 0.7
particle minecraft:trial_spawner_detection_ominous ~ ~-0.8 ~ 0.5 0.2 0.5 0.05 30
